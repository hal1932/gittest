# encoding: utf-8


class Stage(object):

    def __init__(self, index_obj):
        self.__index_obj = index_obj
        self.__is_commited = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            return False

        if not self.__is_commited:
            self.rollback()

        return True

    def add(self, *paths):
        for path in paths:
            self.__index_obj.add(path)

    def remove(self, *paths):
        for path in paths:
            self.__index_obj.remove(path)

    def apply_changes(self):
        self.__index_obj.write()
        self.__is_commited = True

    def rollback(self):
        self.__index_obj.read()


class Index(object):

    @property
    def object(self): return self.__obj

    def __init__(self, obj):
        self.__obj = obj
        self.update()

    def __str__(self):
        return '[{}]'.format(', '.join([x.path for x in self.__obj]))

    def __contains__(self, item):
        return item in self.__obj

    def update(self):
        self.__obj.read()

    def clear(self):
        self.__obj.clear()

    def staging(self):
        return Stage(self.__obj)
