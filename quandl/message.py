class Message:
    ERROR_ARGUMENTS_LIST_FORMAT = 'Your data set must be specified as a string that contains\
        a Quandl code or as a tuple'
    ERROR_AUTHTOKEN_NOT_SUPPORTED = 'The parameter authtoken is no longer supported. \
        For more information please see \
        https://github.com/quandl/quandl-python/blob/master/README.md'
    ERROR_COLUMNS_DATA_NOT_MATCHED = 'The number of columns requested does not match \
        the data returned.'
    ERROR_COLUMN_INDEX_TYPE = 'The column index must be expressed as an integer for %s.'
    ERROR_COLUMN_INDEX_LIST = '%s : column_index must be expressed as a list of \
        integer indexes.'
    ERROR_DATASET_FORMAT = 'Your dataset must either be specified as a string that contains a \
        single Quandl code or an array of Quandl codes'
    ERROR_DATASETS_CODE_MUST_IN_LIST = 'dataset codes must be specified in a list'
    ERROR_FOLDER_ISSUE = 'The folder path specified is incorrect or you do not have \
        permission to access to the folder. Check your settings and try again.'
    ERROR_INVALID_DATABASE_CODE_FROMAT = 'Invalid format used for Quandl database code. \
        The correct format is: `DATABASE_CODE/DATASET_CODE`'
    ERROR_INVALID_DATASET = 'Invalid dataset. Your dataset must be specified as an array \
        of Quandl codes.'
    ERROR_REQUESTED_INDEX_OUT_OF_RANGE = '%s : The requested index %s is out of range. The \
        minimum index is 1 and the maximum index is %s'
    ERROR_REQUESTED_COLUMN_NOT_EXIST = 'Requested column index %s does not exist'

    WARN_DATA_LIMIT_EXCEEDED = 'Data limit exceeded. A maximum of 1 million rows can be returned \
        based on your settings. For more information please see: \
        https://github.com/quandl/quandl-python/blob/master/README.md'
    WARN_PAGE_LIMIT_EXCEEDED = "Page limit exceeded. The first 10,000 rows have been returned. \
        To increase your limit set 'paginate=True'"
    WARN_PARAMS_NOT_SUPPORTED = '%s will no longer supported. Please use %s instead'
