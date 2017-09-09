# encoding: utf-8
from __future__ import print_function
import os
import datetime

os.environ['LIBGIT2'] = r'D:\yuta\Desktop\libgit2-0.26.0\release'
import pygit2


class Commit(object):

    @property
    def hash(self): return self.__obj.id

    @property
    def time(self): return datetime.datetime.fromtimestamp(self.__obj.commit_time)

    @property
    def author(self): return self.__obj.author.name

    @property
    def message(self): return self.__obj.message

    def __init__(self, raw_obj):
        self.__obj = raw_obj


def main():
    repo = pygit2.Repository(os.getcwd())

    head = repo[repo.head.target]
    for x in dir(head): print(x)

    print(head.id, head.message, head.parents)

    for commit_obj in repo.walk(head.id, pygit2.GIT_SORT_TIME):
        commit = Commit(commit_obj)
        print(commit.hash, len(commit_obj.parents), commit.time, commit.author, commit.message)


if  __name__ == '__main__':
    main()
