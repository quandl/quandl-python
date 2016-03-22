# -*- coding: utf-8 -*-

from .api_config import ApiConfig

from .errors.quandl_error import *

from .model.database import Database
from .model.dataset import Dataset
from .model.datatable import Datatable
from .model.data import Data
from .model.merged_dataset import MergedDataset
import copy

def get_table(code, **options):
    paginate = options.pop('paginate')
    data = None
    while True:
        next_options = copy.deepcopy(options)
        next_data = Datatable(code).data(params=next_options)
        next_cursor_id = next_data.meta['next_cursor_id']
        if next_cursor_id is None:
            break
        elif paginate is not True and next_cursor_id is not None:
            print "for more use paginate=True"
            break
        options['qopts.cursor_id'] = next_cursor_id
        if data is None:
            data = next_data
        else:
            data.extend(next_data)
    return data.to_pandas()
