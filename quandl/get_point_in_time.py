from quandl.model.point_in_time import PointInTime
from quandl.errors.quandl_error import LimitExceededError
from .api_config import ApiConfig
from .message import Message
from quandl.errors.quandl_error import InvalidRequestError
import warnings
import copy


def get_point_in_time(datatable_code, **options):
    validate_pit_options(options)
    pit_options = {}

    # Remove the PIT params/keys from the options to not send it as a query params
    for k in ['interval', 'date', 'start_date', 'end_date']:
        if k in options.keys():
            pit_options[k] = options.pop(k)

    if 'paginate' in options.keys():
        paginate = options.pop('paginate')
    else:
        paginate = None

    data = None
    page_count = 0
    while True:
        next_options = copy.deepcopy(options)
        next_data = PointInTime(datatable_code, pit=pit_options).data(params=next_options)

        if data is None:
            data = next_data
        else:
            data.extend(next_data)

        if page_count >= ApiConfig.page_limit:
            raise LimitExceededError(
                Message.WARN_DATA_LIMIT_EXCEEDED % (datatable_code,
                                                    ApiConfig.api_key
                                                    )
            )

        next_cursor_id = next_data.meta['next_cursor_id']

        if next_cursor_id is None:
            break
        elif paginate is not True and next_cursor_id is not None:
            warnings.warn(Message.WARN_PAGE_LIMIT_EXCEEDED, UserWarning)
            break

        page_count = page_count + 1
        options['qopts.cursor_id'] = next_cursor_id
    return data.to_pandas()


def validate_pit_options(options):
    if 'interval' not in options.keys():
        raise InvalidRequestError('option `interval` is required')

    if options['interval'] not in ['asofdate', 'from', 'between']:
        raise InvalidRequestError('option `interval` is invalid')

    if options['interval'] in ['from', 'between']:
        if 'start_date' not in options.keys() or 'end_date' not in options.keys():
            raise InvalidRequestError('options `start_date` and `end_date` are required')
