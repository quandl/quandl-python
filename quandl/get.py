from quandl.errors.quandl_error import InvalidRequestError
from .model.dataset import Dataset
from .model.merged_dataset import MergedDataset
from .utils.api_key_util import ApiKeyUtil
from .message import Message
from six import string_types
import warnings

OLD_TO_NEW_PARAMS = {'authtoken': 'api_key', 'trim_start': 'start_date',
                     'trim_end': 'end_date', 'transformation': 'transform',
                     'sort_order': 'order'}


def get(dataset, **kwargs):
    """Return dataframe of requested dataset from Quandl.
    :param dataset: str or list, depending on single dataset usage or multiset usage
            Dataset codes are available on the Quandl website
    :param str api_key: Downloads are limited to 50 unless api_key is specified
    :param str start_date, end_date: Optional datefilers, otherwise entire
           dataset is returned
    :param str collapse: Options are daily, weekly, monthly, quarterly, annual
    :param str transform: options are diff, rdiff, cumul, and normalize
    :param int rows: Number of rows which will be returned
    :param str order: options are asc, desc. Default: `asc`
    :param str returns: specify what format you wish your dataset returned as,
        either `numpy` for a numpy ndarray or `pandas`. Default: `pandas`
    :returns: :class:`pandas.DataFrame` or :class:`numpy.ndarray`
    Note that Pandas expects timeseries data to be sorted ascending for most
    timeseries functionality to work.
    Any other `kwargs` passed to `get` are sent as field/value params to Quandl
    with no interference.
    """

    _convert_params_to_v3(kwargs)

    data_format = kwargs.pop('returns', 'pandas')

    ApiKeyUtil.init_api_key_from_args(kwargs)

    # Check whether dataset is given as a string
    # (for a single dataset) or an array (for a multiset call)

    # Unicode String
    if isinstance(dataset, string_types):
        dataset_args = _parse_dataset_code(dataset)
        if dataset_args['column_index'] is not None:
            kwargs.update({'column_index': dataset_args['column_index']})
        data = Dataset(dataset_args['code']).data(params=kwargs, handle_column_not_found=True)
    # Array
    elif isinstance(dataset, list):
        args = _build_merged_dataset_args(dataset)
        # handle_not_found_error if set to True will add an empty DataFrame
        # for a non-existent dataset instead of raising an error
        data = MergedDataset(args).data(params=kwargs,
                                        handle_not_found_error=True,
                                        handle_column_not_found=True)
    # If wrong format
    else:
        raise InvalidRequestError(Message.ERROR_DATASET_FORMAT)

    if data_format == 'numpy':
        return data.to_numpy()
    return data.to_pandas()


def _parse_dataset_code(dataset):
    if '.' not in dataset:
        return {'code': dataset, 'column_index': None}
    dataset_temp = dataset.split('.')
    if not dataset_temp[1].isdigit():
        raise ValueError(Message.ERROR_COLUMN_INDEX_TYPE % dataset)
    return {'code': dataset_temp[0], 'column_index': int(dataset_temp[1])}


def _build_merged_dataset_args(datasets):
    merged_dataset_args = []
    for dataset in datasets:
        dataset_code_column = _parse_dataset_code(dataset)
        arg = dataset_code_column['code']
        column_index = dataset_code_column['column_index']
        if column_index is not None:
            arg = (dataset_code_column['code'], {'column_index': [column_index]})
        merged_dataset_args.append(arg)
    return merged_dataset_args


def _convert_params_to_v3(params):
    for k, v in OLD_TO_NEW_PARAMS.items():
        if k in params:
            msg = Message.WARN_PARAMS_NOT_SUPPORTED % (k, v)
            warnings.warn(msg, DeprecationWarning)
            # update to the new query param if not specified already
            if v not in params:
                params[v] = params.pop(k)
