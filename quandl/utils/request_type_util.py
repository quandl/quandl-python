try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from quandl.api_config import ApiConfig


class RequestType(object):
    """ Determines whether a request should be made using a GET or a POST request.
    Default limit of 8000 is set here as it appears to be the maximum for many
    webservers.
    """
    MAX_URL_LENGTH_FOR_GET = 8000
    USE_GET_REQUEST = True  # This is used to simplify testing code

    @classmethod
    def get_request_type(cls, url, **params):
        query_string = urlencode(params['params'])
        request_url = '%s/%s/%s' % (ApiConfig.api_base, url, query_string)
        if RequestType.USE_GET_REQUEST and (len(request_url) < cls.MAX_URL_LENGTH_FOR_GET):
            return 'get'
        else:
            return 'post'
