try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from quandl.api_config import ApiConfig


class RequestType(object):
    MAX_URL_LENGTH_FOR_GET = 8000

    @classmethod
    def get_request_type(cls,url, **params):
        query_string = urlencode(params['params'])
        request_url = '%s/%s/%s' % (ApiConfig.api_base, url, query_string)
        if len(request_url) < cls.MAX_URL_LENGTH_FOR_GET:
            return 'GET'
        else:
            return 'POST'
