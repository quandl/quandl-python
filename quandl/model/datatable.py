import os
from time import sleep

from six.moves.urllib.request import urlopen

from quandl.connection import Connection
from quandl.errors.quandl_error import QuandlError
from quandl.message import Message
from quandl.operations.get import GetOperation
from quandl.operations.list import ListOperation
from quandl.util import Util
from quandl.utils.request_type_util import RequestType
from .data import Data
from .model_base import ModelBase


class Datatable(GetOperation, ListOperation, ModelBase):
    BULK_CHUNK_SIZE = 16 * 1024
    WAIT_GENERATION_INTERVAL = 30

    @classmethod
    def get_path(cls):
        return "%s/metadata" % cls.default_path()

    def data(self, **options):
        if not options:
            options = {'params': {}}
        return Data.page(self, **options)

    def download_file(self, file_or_folder_path, **options):
        if not isinstance(file_or_folder_path, str):
            raise QuandlError(Message.ERROR_FOLDER_ISSUE)

        file_is_ready = False

        while not file_is_ready:
            file_is_ready = self._request_file_info(file_or_folder_path, params=options)
            if not file_is_ready:
                print(Message.LONG_GENERATION_TIME)
                sleep(self.WAIT_GENERATION_INTERVAL)

    def _request_file_info(self, file_or_folder_path, **options):
        url = self._download_request_path()
        code_name = self.code
        options['params']['qopts.export'] = 'true'

        request_type = RequestType.get_request_type(url, **options)

        updated_options = Util.convert_options(request_type=request_type, **options)

        r = Connection.request(request_type, url, **updated_options)

        response_data = r.json()

        file_info = response_data['datatable_bulk_download']['file']

        status = file_info['status']

        if status == 'fresh':
            file_link = file_info['link']
            self._download_file_with_link(file_or_folder_path, file_link, code_name)
            return True
        else:
            return False

    def _download_file_with_link(self, file_or_folder_path, file_link, code_name):
        file_path = file_or_folder_path
        if os.path.isdir(file_or_folder_path):
            file_path = os.path.join(file_or_folder_path,
                                     '{}.{}'.format(code_name.replace('/', '_'), 'zip'))

        res = urlopen(file_link)

        with open(file_path, 'wb') as fd:
            while True:
                chunk = res.read(self.BULK_CHUNK_SIZE)
                if not chunk:
                    break
                fd.write(chunk)

        print(file_path)

    def _download_request_path(self):
        url = self.default_path()
        url = Util.constructed_path(url, {'id': self.code})
        url += '.json'
        return url
