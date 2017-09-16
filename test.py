# encoding: utf-8
from __future__ import print_function
import os
os.environ['LIBGIT2'] = r'D:\yuta\Desktop\libgit2-0.26.0\release'

from Repository import *
import config


# https://github.com/libgit2/pygit2/tree/master/test

def main():
    repo = Repository.from_path(os.getcwd())

    '''
    head = repo.get_head()
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

    repo.checkout_branch(repo.local_master)

    print(repo.directory)
    
    repo.commit_to_branch(repo.local_master, 'hoge', config.USERNAME, config.MAIL_ADDRESS)

    head = repo.get_head()
    for entry in head.object.tree:
        print(entry.id, entry.type, entry.filemode, entry.name)

    index = repo.get_index()
    with index.staging() as stage:
        stage.add('test.py')
        stage.apply_changes()
    repo.commit_to_branch(repo.local_master, 'commit test', config.USERNAME, config.MAIL_ADDRESS)

    #local = repo.local_master
    local = repo.find_or_create_branch('test', checkout=True)
    index = repo.get_index()
    with index.staging() as stage:
        stage.add('test.txt')
        stage.apply_changes()
    repo.commit_to_branch(local, 'add test.txt', config.USERNAME, config.MAIL_ADDRESS)

    cred = RemoteCredentials()
    cred.username = config.USERNAME
    cred.password = config.PASSWORD

    repo.push_to_remote(cred, local)
    '''

    '''
    r = repo.object
    remote = r.remotes['origin']
    remote.fetch()
    remote_master = r.branches.remote['origin/master']
    result, do_fastfoward = r.merge_analysis(remote_master.target)
    if result == pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
        print('local branch is up to date')
    elif result == pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
        if do_fastfoward == 0:
            print('be able to do fastforward-marge and to create the merge-commit')
            print('hoge')
        elif do_fastfoward == 1:
            print('do fastforward-merge')
            print('hoge')
    elif result == pygit2.GIT_MERGE_ANALYSIS_NORMAL:
        print('aaa')
        pass
    '''

    '''
    local_master = repo.local_master
    remote_master = repo.remote_origin_master
    remote = repo.object.remotes[remote_master.remote_name]
    callbacks = Repository.RemoteCallbacks(None)
    refspec = '+{}:{}'.format(local_master.fullname, remote_master.fullname)
    print(refspec)
    progress = remote.fetch([refspec], callbacks=callbacks)
    print(progress.received_bytes, progress.received_objects)
    '''

    head = repo.get_head()
    fetch_head = repo.get_fetch_head()
    diff = repo.object.diff(head.object, fetch_head.object)
    print(diff.stats.format(pygit2.GIT_DIFF_STATS_FULL, 256))
    for patch in diff:
        print(patch.hunks, patch.line_stats)
        delta = patch.delta
        print(delta.status, delta.similarity, delta.is_binary)
        print(delta.old_file.path, delta.new_file.path)

    result, _ = repo.object.merge_analysis(fetch_head.hash)
    print(result)
    if result == pygit2.GIT_MERGE_ANALYSIS_NONE:
        pass
    else:
        if result & pygit2.GIT_MERGE_ANALYSIS_NORMAL != 0:
            print('GIT_MERGE_ANALYSIS_NORMAL')
        if result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD != 0:
            print('GIT_MERGE_ANALYSIS_FASTFORWARD')
        if result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE != 0:
            print('GIT_MERGE_ANALYSIS_UP_TO_DATE')
        if result & pygit2.GIT_MERGE_ANALYSIS_UNBORN != 0:
            print('GIT_MERGE_ANALYSIS_UNBORN')


if __name__ == '__main__':
    main()
