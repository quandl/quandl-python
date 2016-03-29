from quandl.api_config import ApiConfig


class ApiKeyUtil(object):
    @staticmethod
    def init_api_key_from_args(params):
        # set api key
        if 'api_key' in params:
            ApiConfig.api_key = params.pop('api_key')
