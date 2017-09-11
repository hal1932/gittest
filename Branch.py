# encoding: utf-8
import pygit2


class Branch(object):

    @property
    def name(self): return self.__obj.shorthand

    @property
    def fullname(self): return self.__obj.name

    @property
    def target_commit_hash(self): return self.__obj.target

    @property
    def is_head(self): return self.__obj.is_head()

    @property
    def is_checked_out(self): return self.__obj.is_checked_out()

    @property
    def is_symbolic(self): return self.__obj.type == pygit2.GIT_REF_SYMBOLIC

    @property
    def object(self): return self.__obj

    def __init__(self, obj):
        self.__obj = obj

    def remove(self):
        self.__obj.delete()
        self.__obj = None
