# -*- coding: utf-8 -*-

from .api_config import ApiConfig

from .errors.quandl_error import *

from .model.database import Database
from .model.dataset import Dataset
from .model.datatable import Datatable
from .model.data import Data
from .model.merged_dataset import MergedDataset
from .get import get
from .bulkdownload import bulkdownload
import warnings
import copy, os

def get_table(code, **options):
    paginate = None
    if 'paginate' in options.keys(): paginate = options.pop('paginate')
    data = None
    page_count = 0
    while True:
        next_options = copy.deepcopy(options)
        next_data = Datatable(code).data(params=next_options)

        if data is None:
            data = next_data
        else:
            data.extend(next_data)

        if page_count >= ApiConfig.page_limit:
            if os.isatty(0):
                warnings.warn("data over page limit, rest data won't include", UserWarning)
            break

        next_cursor_id = next_data.meta['next_cursor_id']
        if next_cursor_id is None:
            break
        elif paginate is not True and next_cursor_id is not None:
            if os.isatty(0):
                warnings.warn("This is the first page, for more pages, please use 'paginate=True'", UserWarning)
            break
        page_count = page_count + 1
        options['qopts.cursor_id'] = next_cursor_id
    return data.to_pandas()
