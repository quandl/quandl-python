from quandl.errors.quandl_error import InvalidRequestError
from .utils.api_key_util import ApiKeyUtil
from .model.database import Database


def bulkdownload(database, **kwargs):
    """Downloads an entire database.
    :param str database: The database code to download
    :param str filename: The filename for the download. \
    If not specified, will download to the current working directory
    :param str api_key: Most databases require api_key for bulk download
    :param str download_type: 'partial' or 'complete'. \
    See: https://www.quandl.com/docs/api#database-metadata
    """

    # discourage users from using authtoken
    if 'authtoken' in kwargs:
        error_msg = "Parameter authtoken is no longer supported. \
        For more information please see \
        https://github.com/quandl/quandl-python/blob/master/README.md"
        raise InvalidRequestError(error_msg)

    ApiKeyUtil.init_api_key_from_args(kwargs)

    filename = kwargs.pop('filename', '.')
    return Database(database).bulk_download_to_file(filename, params=kwargs)
