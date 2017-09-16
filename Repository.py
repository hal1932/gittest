# encoding: utf-8
import os

import pygit2

from Commit import *
from Branch import *
from Index import *


class Status(object):

    def __init__(self, dic):
        def extract(target):
            return [path for path, status in dic.items() if status == target]

        self.index_new = extract(pygit2.GIT_STATUS_INDEX_NEW)
        self.index_modified = extract(pygit2.GIT_STATUS_INDEX_MODIFIED)
        self.index_deleted = extract(pygit2.GIT_STATUS_INDEX_DELETED)

        self.new = extract(pygit2.GIT_STATUS_WT_NEW)
        self.modified = extract(pygit2.GIT_STATUS_WT_MODIFIED)
        self.deleted = extract(pygit2.GIT_STATUS_WT_DELETED)

        self.current = extract(pygit2.GIT_STATUS_CURRENT)
        self.conflicted = extract(pygit2.GIT_STATUS_CONFLICTED)
        self.ignored = extract(pygit2.GIT_STATUS_IGNORED)

    def __str__(self):
        return str(self.__dict__)


class RemoteCredentials(object):

    def __init__(self):
        self.username = None
        self.password = None

        self.id_rsa_pub = None
        self.id_rsa = None


class Repository(object):

    # region class __RemoteCallbacks
    class __RemoteCallbacks(pygit2.RemoteCallbacks):

        def __init__(self, credentials):
            self.__username = credentials.username
            self.__password = credentials.password

            self.__id_rsa_pub = credentials.id_rsa_pub
            self.__id_rsa = credentials.id_rsa

        '''
        def certificate_check(self, certificate, valid, host):
            print('[certificate_check]', certificate, valid, host)
            return True
        '''

        def credentials(self, url, username_from_url, allowed_types):
            # print('[credentials]', url, username_from_url, allowed_types)
            if allowed_types == pygit2.GIT_CREDTYPE_SSH_KEY:
                return pygit2.Keypair('git', self.__id_rsa_pub, self.__id_rsa, '')
            elif allowed_types == pygit2.GIT_CREDTYPE_USERPASS_PLAINTEXT:
                return pygit2.UserPass(self.__username, self.__password)
            else:
                raise RuntimeError('unsupported authentication type: {}'.format(allowed_types))

        '''
        def push_update_reference(self, refname, message):
            print('[push_update_reference]', refname, message)
        '''
    # endregion

    @staticmethod
    def from_path(directory):
        obj = pygit2.Repository(directory)
        return Repository(obj)

    @property
    def object(self): return self.__obj

    @property
    def directory(self): return self.__obj.workdir

    @property
    def master(self): return self.get_branch('master')

    def __init__(self, obj):
        self.__obj = obj

    # region Commit
    def get_head_commit(self):
        return Commit(self.__obj[self.__head_obj_id()])

    def get_branch_target_commit(self, branch):
        return Commit(self.__obj[branch.target_commit_hash])

    def get_commit(self, hash):
        return Commit(self.__obj[hash])

    def find_commit(self, hash):
        obj = self.__find_obj(hash)
        if obj is not None:
            return Commit(obj)
        return None

    def enumerate_commits(self):
        for commit_obj in self.__obj.walk(self.__head_obj_id(), pygit2.GIT_SORT_TIME):
            yield Commit(commit_obj)

    def commit_to_branch(self, branch, message, user, email):
        author = pygit2.Signature(user, email)
        commiter = author
        tree = self.__obj.index.write_tree()
        commit_hash = self.__obj.create_commit(
            branch.fullname,
            author, commiter, message,
            tree,
            [branch.target_commit_hash]
        )
        return self.get_commit(commit_hash)

    # endregion

    # region Branch
    def get_branch(self, name):
        return Branch(self.__obj.branches[name])

    def get_local_branch(self, name):
        return Branch(self.__obj.branches.local[name])

    def get_remote_branch(self, name):
        return Branch(self.__obj.branches.remote[name])

    def find_branch(self, name):
        return Repository.__find_branch(self.__obj.branches, name)

    def find_local_branch(self, name):
        return Repository.__find_branch(self.__obj.branches.local, name)

    def find_remote_branch(self, name):
        return Repository.__find_branch(self.__obj.branches.remote, name)

    def enumerate_branches(self):
        return Repository.__enumerate_branches(self.__obj.branches)

    def enumerate_local_branches(self):
        return Repository.__enumerate_branches(self.__obj.branches.local)

    def enumerate_remote_branches(self):
        return Repository.__enumerate_branches(self.__obj.branches.remote)

    def create_local_branch(self, name, checkout=False):
        branch_obj = self.__obj.branches.local.create(name, self.__obj.head.get_object())
        branch = Branch(branch_obj)

        if checkout:
            self.checkout_branch(branch)

        return branch

    def find_or_create_branch(self, name, checkout=False):
        branch = self.find_local_branch(name)
        if branch is None:
            branch = self.create_local_branch(name)

        if checkout:
            self.checkout_branch(branch)

        return branch

    def checkout_branch(self, branch):
        self.__obj.checkout(branch.object)

    def push_to_remote(self, credentials, branch, remote='origin'):
        callbacks = Repository.__RemoteCallbacks(credentials)
        remote_branch = self.object.remotes[remote]
        remote_branch.push([branch.fullname], callbacks)
    # endregion

    # region Status
    def get_status(self):
        return Status(self.__obj.status())
    # endregion

    # region Index
    def get_index(self):
        return Index(self.__obj.index)

    def force_reset_index(self):
        index_file = os.path.join(os.getcwd(), '.git', 'index')
        if os.path.isfile(index_file):
            os.remove(index_file)
        self.__obj.reset(self.__head_obj_id(), pygit2.GIT_RESET_MIXED)
        self.reset(Repository.ROLLBACK_HEAD_INDEX)
    # endregion

    # region reset
    RESET_SOFT = pygit2.GIT_RESET_SOFT
    RESET_MIXED = pygit2.GIT_RESET_MIXED
    RESET_HARD = pygit2.GIT_RESET_HARD

    ROLLBACK_HEAD = RESET_SOFT
    ROLLBACK_HEAD_INDEX = RESET_MIXED
    ROLLBACK_HEAD_INDEX_FILES = RESET_HARD

    def reset(self, option=ROLLBACK_HEAD_INDEX):
        self.__obj.reset(self.__head_obj_id(), option)
    # endregion

    # region private
    @staticmethod
    def __find_branch(branches, name):
        obj = branches.get(name)
        if obj is not None:
            return Branch(obj)
        return None

    @staticmethod
    def __enumerate_branches(branches):
        for branch_name in branches:
            branch_obj = branches[branch_name]
            yield Branch(branch_obj)

    def __find_obj(self, id):
        # get() はオブジェクトが存在しない場合に None を返すはずだけど
        # 実際には ValueError を吐くから自前でハンドリングする
        try:
            return self.__obj.get(id)
        except ValueError:
            return None

    def __head_obj_id(self):
        return self.__obj.head.target
    # endregion


