try:
    from urllib.parse import urlencode
    from urllib.request import urlopen
except ImportError:
    from urllib import urlencode
    from urllib import urlopen

from time import sleep
import os

from quandl.api_config import ApiConfig
from quandl.connection import Connection
from quandl.util import Util
from quandl.errors.quandl_error import QuandlError
from quandl.operations.get import GetOperation
from quandl.operations.list import ListOperation

from .model_base import ModelBase
from quandl.message import Message
from .data import Data


class Datatable(GetOperation, ListOperation, ModelBase):
    BULK_CHUNK_SIZE = 16 * 1024

    @classmethod
    def get_path(cls):
        return "%s/metadata" % cls.default_path()

    def data(self, **options):
        updated_options = Util.convert_options(**options)
        return Data.page(self, **updated_options)

    def bulk_download_file(self, file_or_folder_path, **options):
        if not isinstance(file_or_folder_path, str):
            raise QuandlError(Message.ERROR_FOLDER_ISSUE)

        return self._url_request(file_or_folder_path, **options)

    def _url_request(self, file_or_folder_path, **options):
        url = self._download_request_path()
        code_name = self.code
        if 'params' not in options:
            options['params'] = {}
        if ApiConfig.api_key:
            options['params']['api_key'] = ApiConfig.api_key
        if ApiConfig.api_version:
            options['params']['api_version'] = ApiConfig.api_version

        if list(options.keys()):
            url += '.json?qopts.export=true&' + urlencode(options['params'])

        r = Connection.request('get', url, **options)
        response_data = r.json()

        status = response_data['datatable_bulk_download']['file']['status']

        if status == 'fresh':
            file_link = response_data['datatable_bulk_download']['file']['link']

            file_path = file_or_folder_path
            if os.path.isdir(file_or_folder_path):
                file_path = file_or_folder_path + '/' + code_name.replace('/', '_') + '.zip'

            res = urlopen(file_link)

            with open(file_path, 'wb') as fd:
                while True:
                    chunk = res.read(self.BULK_CHUNK_SIZE)
                    if not chunk:
                        break
                    fd.write(chunk)

            return file_path
        else:
            print(Message.LONG_GENERATION_TIME)
            self._url_request(file_or_folder_path, **options)
            sleep(30)

    def _download_request_path(self):
        url = self.default_path()
        url = Util.constructed_path(url, {'id': self.code})
        return url
