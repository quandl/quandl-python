from quandl.errors.quandl_error import InvalidRequestError
from .utils.api_key_util import ApiKeyUtil
from .model.datatable import Datatable
from .message import Message

def bulkdownloadtable(datatable_code, **kwargs):
    """Downloads an entire table as a zip file.
    :param str datatable_code: The datatable code to download, such as MER/F1
    :param str filename: The filename for the download. \
    If not specified, will download to the current working directory
    :param str api_key: Most databases require api_key for bulk download
    """

    # discourage users from using authtoken
    if 'authtoken' in kwargs:
        raise InvalidRequestError(Message.ERROR_AUTHTOKEN_NOT_SUPPORTED)

    ApiKeyUtil.init_api_key_from_args(kwargs)

    filename = kwargs.pop('filename', '.')
    return Datatable(datatable_code).bulk_download_file(filename, params=kwargs)
