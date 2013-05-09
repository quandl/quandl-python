# -*- coding: utf-8 -*-
"""
Quandl's API for Python.

Currently supports getting, searching, and pushing datasets.

"""
from __future__ import (print_function, division, absolute_import,
                        unicode_literals)
import pickle
import datetime
import json
import pandas as pd
import re

from dateutil import parser
from numpy import genfromtxt

try:
    from urllib.error import HTTPError  # Python 3
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen
except ImportError:
    from urllib import urlencode  # Python 2
    from urllib2 import HTTPError, Request, urlopen



QUANDL_API_URL = 'http://www.quandl.com/api/v1/'


def get(dataset, **kwargs):
    """Return dataframe of requested dataset from Quandl.

    :param str dataset: Dataset codes are available on the Quandl website
    :param str authtoken: Downloads are limited to 10 unless token is specified
    :param str trim_start, trim_end: Optional datefilers, otherwise entire
           dataset is returned
    :param str collapse: Options are daily, weekly, monthly, quarterly, annual
    :param str transformation: options are diff, rdiff, cumul, and normalize
    :param int rows: Number of rows which will be returned
    :param str sort_order: options are asc, desc. Default: `asc`
    :param str returns: specify what format you wish your dataset returned as,
        either `numpy` for a numpy ndarray or `pandas`. Default: `pandas`
    :returns: :class:`pandas.DataFrame` or :class:`numpy.ndarray`

    Note that Pandas expects timeseries data to be sorted ascending for most
    timeseries functionality to work.

    Any other `kwargs` passed to `get` are sent as field/value params to Quandl
    with no interference.

    """
    kwargs.setdefault('sort_order', 'asc')

    auth_token = _getauthtoken(kwargs.pop('authtoken', ''))
    trim_start = _parse_dates(kwargs.pop('trim_start', None))
    trim_end = _parse_dates(kwargs.pop('trim_end', None))
    returns = kwargs.get('returns', 'pandas')

    url = QUANDL_API_URL + 'datasets/{}.csv?'.format(dataset)
    url = _append_query_fields(url,
                               auth_token=auth_token,
                               trim_start=trim_start,
                               trim_end=trim_end,
                               **kwargs)

    if returns == 'numpy':
        try:
            u = urlopen(url)
            array = genfromtxt(u, names=True, delimiter=',', dtype=None)
            return array
        except IOError as e:
            print("url:", url)
            raise Exception("Parsing Error! {}".format(e))
        except HTTPError as e:
            print("url:", url)
            raise Exception("Error Downloading! {}".format(e))
    else: # assume pandas is requested
        urldata = _download(url)
        print("Returning Dataframe for ", dataset)
        return urldata


def push(data, code, name, authtoken='', desc='', override=False):
    """Upload a pandas Dataframe to Quandl and returns link to the dataset.

    :param data: (required), pandas ts or numpy array
    :param str code: (required), Dataset code
                 must consist of only capital letters, numbers, and underscores
    :param str name: (required), Dataset name
    :param str authtoken: (required), to upload data
    :param str desc: (optional), Description of dataset
    :param bool overide: (optional), whether to overide dataset of same code
    :returns: :str: link to uploaded dataset

    """
    override = str(override).lower()
    token = _getauthtoken(authtoken)
    if token == '':
        error = ("You need an API token to upload your data to Quandl, "
                 "please see www.quandl.com/API for more information.")
        raise Exception(error)

    _pushcodetest(code)
    datestr = ''

    # Verify and format the data for upload.
    if not isinstance(data, pd.core.frame.DataFrame):
        error = "only pandas data series are accepted for upload at this time"
        raise ValueError(error)

    # check if indexed by date
    data_interm = data.to_records()
    index = data_interm.dtype.names
    datestr += ','.join(index) + '\n'

    for i in data_interm:
        if isinstance(i[0], datetime.datetime):
            datestr += i[0].date().isoformat()
        else:
            # Check if index is a date
            try:
                datestr += _parse_dates(str(i[0]))
            except ValueError:
                error = ("Please check your indices, one of them is "
                         "not a recognizable date")
                raise Exception(error)
        for n in i:
            if isinstance(n, (float, int)):
                datestr += ',' + str(n)
        datestr += '\n'

    params = {'name': name,
              'code': code,
              'description': desc,
              'update_or_create': override,
              'data': datestr}

    url = QUANDL_API_URL + 'datasets.json?auth_token=' + token
    jsonreturn = _htmlpush(url, params)
    if (jsonreturn['errors']
        and jsonreturn['errors']['code'][0] == 'has already been taken'):
        error = ("You are trying to overwrite a dataset which already "
                 "exists on Quandl. If this is what you wish to do please "
                 "recall the function with overide = True")
        raise ValueError(error)

    rtn = ('http://www.quandl.com/' + jsonreturn['source_code'] + '/' +
           jsonreturn['code'])
    return rtn


def search(query,source = None, page = 1, authotoken = None):
   """Return array of dictionaries of search results.

      :param str query: (required), query to search with
      :param str source: (optional), source to search
      :param +'ve int: (optional), page number of search 
      :param str authotoken: (optional) Quandl auth token for extended API access
      :returns: :array: search results

      """
      token = _getauthtoken(authtoken)
      search_url = 'http://www.quandl.com/api/v1/datasets.json?query='
      parsedquery = re.sub(" ", "+", query)
      url = search_url + parsedquery
      if token:
          url += '&auth_token=' + token
      if source:
          url += '&source_code=' + source
      url += '&page=' + str(page)
      text= urlopen(url).read()
      data = json.loads(text)
      try:
          datasets = data['docs']
      except TypeError:
          raise TypeError("There are no matches for this search")
      datalist = []
      for i in range(len(datasets)):
          temp_dict ={}
          temp_dict['name'] = datasets[i]['name']
          temp_dict['code'] = datasets[i]['source_code'] + '/' + datasets[i]['code']
          temp_dict['desc'] = datasets[i]['description']
          temp_dict['freq'] = datasets[i]['frequency']
          temp_dict['colname'] = datasets[i]['column_names']
          datalist.append(temp_dict)
      return datalist


# returns None is date is None
def _parse_dates(date):
    if date is None:
        return date
    if isinstance(date, datetime.datetime):
        return date.date().isoformat()
    if isinstance(date, datetime.date):
        return date.isoformat()
    try:
        date = parser.parse(date)
    except ValueError:
        raise ValueError("{} is not recognised a date.".format(date))
    return date.date().isoformat()


def _download(url):
    dframe = pd.read_csv(url, index_col=0, parse_dates=True)
    return dframe


def _htmlpush(url, raw_params):
    page = url
    params = urlencode(raw_params)
    request = Request(page, params)
    page = urlopen(request)
    return json.loads(page.read())


def _pushcodetest(code):
    regex = re.compile('[^0-9A-Z_]')
    if regex.search(code):
        error = ("Your Quandl Code for uploaded data must consist of only "
                 "capital letters, underscores and capital numbers.")
        raise Exception(error)
    return code


def _getauthtoken(token):
    """Return and save API token to a pickle file for reuse."""
    try:
        savedtoken = pickle.load(open('authtoken.p', 'rb'))
    except IOError:
        savedtoken = False
    if token:
        pickle.dump(token, open('authtoken.p', 'wb'))
        print("Token {} activated and saved for later use.".format(token))
    elif not savedtoken and not token:
        print("No authentication tokens found: usage will be limited.")
        print("See www.quandl.com/api for more information.")
    elif savedtoken and not token:
        token = savedtoken
        print("Using cached token {} for authentication.".format(token))
    return token


# In lieu of urllib's urlencode, as this handles None values by ignoring them.
def _append_query_fields(url, **kwargs):
    field_values = ['{}={}'.format(key, val)
                    for key, val in kwargs.items() if val]
    return url + '&'.join(field_values)
