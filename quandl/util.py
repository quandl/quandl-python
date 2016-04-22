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
    def convert_to_dates(dic_or_list):
        if isinstance(dic_or_list, dict):
            for k, v in list(dic_or_list.items()):
                dic_or_list[k] = Util.convert_to_dates(v)
        elif isinstance(dic_or_list, list):
            for idx, v in enumerate(dic_or_list):
                dic_or_list[idx] = Util.convert_to_dates(v)
        else:
            return Util.convert_to_date(dic_or_list)

        return dic_or_list

    @staticmethod
    def convert_to_date(value):
        if isinstance(value, string_types) and re.search(r'^\d{4}-\d{2}-\d{2}$', value):
            # convert to datetime.date
            return dateutil.parser.parse(value).date()
        elif isinstance(value, string_types) and re.search(r'^\d{4}-\d{2}-\d{2}T[\d:\.]+Z$', value):
            # convert to datetime.datetime, default timezone is utc
            return dateutil.parser.parse(value)
        else:
            return value

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
        if meta is None:
            return []

        # Dataset API call
        if 'column_names' in meta.keys():
            the_list = [Util.methodize(x) for x in meta['column_names']]
            return list(the_list)
        # Datatable API call
        elif 'columns' in meta.keys():
            return list([Util.methodize(x) for x in meta['columns']])
        else:
            return []
