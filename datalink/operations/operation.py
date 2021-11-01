from inflection import (underscore, pluralize)


class Operation(object):
    @classmethod
    def default_path(cls):
        return "%s/:id" % cls.lookup_key()

    @classmethod
    def lookup_key(cls):
        return underscore(pluralize(cls.__name__))
