# encoding: utf-8
from __future__ import print_function
import os
os.environ['LIBGIT2'] = r'D:\yuta\Desktop\libgit2-0.26.0\release'

from Repository import *
import config


def main():
    repo = Repository.from_path(os.getcwd())

    '''
    head = repo.get_head_commit()
    print(head.hash, head.message, head.author)

    for commit in repo.enumerate_commits():
        print(commit.hash, commit.time, commit.author, commit.committer, commit.message)
        print([p.hash for p in commit.parents])

    for branch in repo.enumerate_branches():
        print(branch.name, branch.fullname, branch.target_commit_hash, branch.is_head, branch.is_checked_out, branch.is_symbolic)
        commit = repo.get_branch_target_commit(branch)
        print(commit.hash)

    print(repo.find_branch('origin/master'))
    print(repo.get_status())

    index = repo.get_index()
    print(index, '.gitattributes' in index, 'hoge' in index)

    with index.staging() as stage:
        stage.add('Index.py')
        print(index)
        print(repo.get_status())
    print(index)
    print(repo.get_status())

    test_branch = repo.find_or_create_branch('test')
    # test_branch.remove()
    repo.checkout_branch(test_branch)
    print(test_branch)

    repo.checkout_branch(repo.master)

    print(repo.directory)
    
    repo.commit_to_branch(repo.master, 'hoge', 'hal1932', 'yu.arai.19@gmail.com')

    head = repo.get_head_commit()
    for entry in head.object.tree:
        print(entry.id, entry.type, entry.filemode, entry.name)

    index = repo.get_index()
    with index.staging() as stage:
        stage.add('test.py')
        stage.apply_changes()
    repo.commit_to_branch(repo.master, 'commit test', 'hal1932', 'yu.arai.19@gmail.com')
    '''

    master = repo.master
    remote_origin = repo.object.remotes['origin']
    remote_origin.push([master.fullname], RemoteCallbacks())


class RemoteCallbacks(pygit2.RemoteCallbacks):

    def credentials(self, url, username_from_url, allowed_types):
        print(url, username_from_url, allowed_types)
        if allowed_types & pygit2.GIT_CREDTYPE_SSH_KEY != 0:
            print('ssh_key')
        elif allowed_types & pygit2.GIT_CREDTYPE_USERPASS_PLAINTEXT != 0:
            return pygit2.UserPass(config.USERNAMWE, config.PASSWORD)
        else:
            raise RuntimeError('unsupported authentication type: {}'.format(allowed_types))

    def push_update_reference(self, refname, message):
        print(refname, message)


if __name__ == '__main__':
    main()
