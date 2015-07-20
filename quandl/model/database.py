try:
    from urllib.parse import urlparse
    from urllib.parse import urlencode
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode

from os.path import basename

from quandl.api_config import ApiConfig
from quandl.connection import Connection
from quandl.util import Util
from quandl.errors.quandl_error import QuandlError
from quandl.operations.get import GetOperation
from quandl.operations.list import ListOperation
from .model_base import ModelBase


class Database(GetOperation, ListOperation, ModelBase):
    BULK_CHUNK_SIZE = 512

    def bulk_download_url(self, **options):
        url = self.default_path() + '/data'
        if 'path_only' not in options or not options['path_only']:
            url = ApiConfig.api_base + '/' + url
        url = Util.constructed_path(url, {'id': self.database_code})

        params = {}
        if 'download_type' in options:
            params['download_type'] = options['download_type']
        if ('include_key' not in options or options['include_key']) \
                and ApiConfig.api_key:
            params['api_key'] = ApiConfig.api_key

        if list(params.keys()):
            url += '?' + urlencode(params)

        return url

    def bulk_download_to_file(self, folder_path, **options):
        if not isinstance(folder_path, str):
            raise QuandlError('You must present a valid folder path.')

        options = Util.merge_to_dicts({'include_key': True, 'path_only': True}, options)
        path_url = self.bulk_download_url(**options)

        r = Connection.request('get', path_url, stream=True)
        file_path = folder_path + '/' + basename(urlparse(r.url).path)
        with open(file_path, 'wb') as fd:
            for chunk in r.iter_content(self.BULK_CHUNK_SIZE):
                fd.write(chunk)

        return file_path

    def datasets(self, **options):
        params = {'database_code': self.database_code, 'query': '', 'page': 1}
        options = Util.merge_options('params', params, **options)
        return Dataset.all(**options)

from .dataset import Dataset
