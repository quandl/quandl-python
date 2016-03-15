from quandl.api_config import ApiConfig
import warnings
import os


class ApiKeyUtil(object):
    @staticmethod
    def init_api_key_from_args(params):
        # set api key
        if 'api_key' in params:
            ApiConfig.api_key = params.pop('api_key')
        # issue warning if api key was previously
        # set and now is not
        elif (ApiConfig.api_key is not None) and os.isatty(0):
            warn_msg = "To ensure your api key is properly configured, please see: \
https://github.com/quandl/quandl-python/blob/master/README.md"
            warnings.warn(warn_msg, UserWarning)
