# encoding: utf-8
import datetime


class Commit(object):

    @property
    def hash(self): return self.__obj.id

    @property
    def time(self): return datetime.datetime.fromtimestamp(self.__obj.commit_time)

    @property
    def author(self): return self.__obj.author.name

    @property
    def committer(self): return self.__obj.committer.name

    @property
    def message(self): return self.__obj.message.strip()

    @property
    def parents(self): return [Commit(obj) for obj in self.__obj.parents]

    @property
    def object(self): return self.__obj

    def __init__(self, obj):
        self.__obj = obj
