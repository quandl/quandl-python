from inflection import parameterize
import dateutil.parser
import re
from six import string_types


class Util(object):
    @staticmethod
    def constructed_path(path, params={}):
        for key in list(params.copy().keys()):
            modified_path = path.replace(":%s" % key, str(params[key]))
            if modified_path != path:
                params.pop(key, None)
                path = modified_path
        return path

    # http://stackoverflow.com/questions/38987/how-can-i-merge-two-python-dictionaries-in-a-single-expression
    @staticmethod
    def merge_to_dicts(x, y):
        z = x.copy()
        z.update(y)
        return z

    @staticmethod
    def methodize(string):
        return parameterize(string.replace(r'.', '')).replace(r'-', '_')

    @staticmethod
    def merge_options(key, dic, **options):
        updated = dic
        # try to merge if options already has key, otherwise just assign
        if key in options:
            # respect values in options over hash
            updated = Util.merge_to_dicts(dic, options[key])
        options[key] = updated
        return options

    @staticmethod
    def convert_to_dates(dic):
        if not isinstance(dic, dict):
            return dic
        for k, v in list(dic.items()):
            if isinstance(v, string_types) and re.search(r'^\d{4}-\d{2}-\d{2}$', v):
                # convert to datetime.date
                dic[k] = dateutil.parser.parse(v).date()
            elif isinstance(v, string_types) and re.search(r'^\d{4}-\d{2}-\d{2}T[\d:\.]+Z$', v):
                # convert to datetime.datetime, default timezone is utc
                dic[k] = dateutil.parser.parse(v)
            elif isinstance(v, list):
                list(map(lambda x: Util.convert_to_dates(x), v))
            elif isinstance(v, dict):
                Util.convert_to_dates(v)
        return dic

    @staticmethod
    def convert_options(**options):
        new_options = dict()
        if 'params' in options.keys():
            for key, value in options['params'].items():
                is_dict = False
                if isinstance(value, list):
                    key = key + '[]'
                else:
                    if isinstance(value, dict) and value != {}:
                        new_value = dict()
                        is_dict = True
                        old_key = key
                        for k, v in value.items():
                            key = key + '.' + k
                            if isinstance(v, list):
                                key = key + '[]'
                            new_value[key] = v
                            key = old_key

                if is_dict:
                    new_options.update(new_value)
                else:
                    new_options[key] = value
        return {'params': new_options}

    @staticmethod
    def convert_to_columns_list(meta, type):
        columns = []
        for key in meta:
            columns.extend([key[type]])
        return columns

    @staticmethod
    def convert_column_names(meta):
        converted_column_names = None
        if 'column_names' in meta.keys():
            the_list = [Util.methodize(x) for x in meta['column_names']]
            return list(the_list)
        else:
            return list([Util.methodize(x) for x in meta['columns']])