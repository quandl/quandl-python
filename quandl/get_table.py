from quandl.model.datatable import Datatable
from .api_config import ApiConfig
import warnings
import copy
import os


def get_table(code, **options):
    if 'paginate' in options.keys():
        paginate = options.pop('paginate')
    else:
        paginate = None

    if 'returns' in options.keys():
        returns = options.pop('returns')
    else:
        returns = None

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
                warnings.warn("This is the first page, for more pages, " +
                              "please use 'paginate=True'", UserWarning)
            break
        page_count = page_count + 1
        options['qopts.cursor_id'] = next_cursor_id

    if returns == 'numpy':
        return data.to_numpy()
    elif returns == 'csv':
        return data.to_csv()
    else:
        return data.to_pandas()
