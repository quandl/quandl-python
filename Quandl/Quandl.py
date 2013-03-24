import pandas as pd
import pickle
from dateutil import parser
import urllib2
#TODO:Needs more debugging and tests,only a limited amount of testing done.


def get(dataset, authtoken='', startdate=None, enddate=None, frequency=None):

    """Returns a Pandas dataframe object from datasets at http://www.quandl.com/
    Download limits are extended if authtoken is obtained from a registered account.

:param dataset: Dataset codes are available on the Quandl website.
:param authtoken: Downloads are limited to 10 unless token is specified.
:param startdate,enddate:Dateranges specif
:param frequency: options are daily,weekly,monthly,quarterly,annual
:returns Pandas Dataframe indexed by date
"""
    allowedfreq = ['daily', 'weekly', 'monthly', 'quarterly', 'annual']
    token = _getauthtoken(authtoken)
    url = 'http://www.quandl.com/api/v1/datasets/%s.csv?' % dataset
    if token:
        url += 'auth_token=%s' % token
    if startdate and not enddate:
        startdate = _parse_dates(startdate)
        url += '&trim_start=%s' % startdate
    elif startdate and enddate:
        startdate, enddate = _parse_dates(startdate), _parse_dates(enddate)
        url += '&trim_start=%s&trim_end=%s' % (startdate, enddate)
    if frequency and frequency not in allowedfreq:
        error = 'Incorrect frequency specified. Use one of the following ' + ",".join(allowedfreq)
        raise Exception(error)
    elif frequency:
        url += '&collapse=%s' % frequency
    urldata = _download(url)
    print 'Returning Dataframe for ', dataset
    return urldata


def _parse_dates(date):
    try:
        date = parser.parse(date)
    except ValueError:
        raise Exception('%s is not recognised a date' % date)
    return date.strftime('%Y-%m-%d')


def _download(url):
    try:
        dframe = pd.read_csv(url, index_col=0, parse_dates=True)
        return dframe
    except urllib2.HTTPError as e:
        print 'url:',url
        raise Exception('Error Downloading! %s' %e)


def _getauthtoken(token):
    """If a token is specified saves to a pickle file for reuse."""
    try:
        savedtoken = pickle.load(open('authtoken.p', 'rb'))
    except IOError:
        savedtoken = False
    if token:
        pickle.dump(token, open('authtoken.p', 'wb'))
        print 'Token %s activated and saved for later use' % token
    elif not savedtoken and not token:
        print "No authentication tokens found,usage will be limited "
    elif savedtoken and not token:
        token = savedtoken
        print 'Using cached token %s for authentication ' % token
    return token
