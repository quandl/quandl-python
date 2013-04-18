# -*- coding: utf-8 -*-
"""
Quandl's API for Python.

Currently supports getting and pushing datasets.

"""
from __future__ import (print_function, division, absolute_import,
                        unicode_literals)
import pickle
import datetime
import pandas as pd

from dateutil import parser
from numpy import genfromtxt

try:
    from urllib.error import HTTPError  # Python 3
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen
except ImportError:
    from urllib import urlencode  # Python 2
    from urllib2 import HTTPError, Request, urlopen



def get(dataset, authtoken='', trim_start=None, trim_end=None, frequency=None,
        transformation=None, rows=None, sort='asc', returns='pandas'):
    """Returns a Pandas dataframe object from datasets at http://www.quandl.com

    :param dataset: Dataset codes are available on the Quandl website.
    :param authtoken: Downloads are limited to 10 unless token is specified.
    :param trim_start,trim_end: Optional datefilers, otherwise entire dataset
           is returned
    :param frequency: options are daily,weekly,monthly,quarterly,annual
    :param transformation: options are diff, rdiff, cumul, and normalize.
    :param rows: Number of rows which will be returned.
    :param sort: options are asc, desc (defaults to asc)
    :param returns: specify what format you wish your dataset returned as.
    :returns pandas Dataframe indexed by date.

    Note that Pandas expects timeseries data to be sorted ascending for most
    timeseries functionality to work.

    """
    token = _getauthtoken(authtoken)
    trim_start, trim_end = map(_parse_dates, (trim_start, trim_end))

    url = 'http://www.quandl.com/api/v1/datasets/{}.csv?'.format(dataset)
    url = _append_query_fields(url, auth_token=token,
                               transformation=transformation,
                               collapse=frequency, rows=rows, sort_order=sort,
                               trim_start=trim_start, trim_end=trim_end)

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

    :param data: Required, pandas ts or numpy array
    :param code: Required, code to 
    :param name: Dataset name, must consist of only capital letters,
                 numbers, and underscores
    :param authtoken: Required to upload data
    :param desc: Description of dataset
    :param overide: whether to overide dataset of same name
    :returns link to uploaded data

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
        raise Exception(error)

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
            except:
                error = ("Please check your indices, one of them is "
                         "not a recognizable date")
                raise Exception(error)
        for n in i:
            if isinstance(n, float) or isinstance(n, int):
                datestr += ',' + str(n)
        datestr += '\n'

    params = {'name': name,
              'code': code,
              'description': desc,
              'update_or_create': override,
              'data': datestr}

    url = 'http://www.quandl.com/api/v1/datasets.json?auth_token=' + token
    jsonreturn = _htmlpush(url, params)
    if (jsonreturn['errors']
        and jsonreturn['errors']['code'][0] == 'has already been taken'):
        error = ("You are trying to overwrite a dataset which already "
                 "exists on Quandl. If this is what you wish to do please "
                 "recall the function with overide = True")
        raise Exception(error)

    rtn = ('http://www.quandl.com/' + jsonreturn['source_code'] + '/' +
           jsonreturn['code'])
    return rtn


# Helper function to parse dates with None fallback
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
        raise Exception("{} is not recognised a date.".format(date))
    return date.date().isoformat()


# Helper function for actually making API call and downloading the file
def _download(url):
    try:
        dframe = pd.read_csv(url, index_col=0, parse_dates=True)
        return dframe
    except pd._parser.CParserError as e:
        print("url:", url)
        raise Exception("Error Reading Data! {}".format(e))
    except HTTPError as e:
        print("url:", url)
        raise Exception("Error Downloading! {}".format(e))


# Helper function to make html push
def _htmlpush(url, raw_params):
    import json
    page = url
    params = urlencode(raw_params)
    request = Request(page, params)
    page = urlopen(request)
    return json.loads(page.read())


def _pushcodetest(code):
    import re
    regex = re.compile('[^0-9A-Z_]')
    if regex.search(code):
        error = ("Your Quandl Code for uploaded data must consist of only "
                 "capital letters, underscores and capital numbers.")
        raise Exception(error)
    return code


def _getauthtoken(token):
    """Return and dave API token to a pickle file for reuse."""
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

