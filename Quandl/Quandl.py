import pandas as pd
import pickle
from dateutil import parser
import urllib2
from numpy import genfromtxt
#TODO:Needs more debugging and tests,only a limited amount of testing done.


def get(dataset, authtoken='', startdate=None, enddate=None, frequency=None, transformation=None, rows = None, returns = "pandas"):

    """Returns a Pandas dataframe object from datasets at http://www.quandl.com/
    Download limits are extended if authtoken is obtained from a registered account.

:param dataset: Dataset codes are available on the Quandl website.
:param authtoken: Downloads are limited to 10 unless token is specified.
:param startdate,enddate:Optional datefilers,otherwise entire dataset is returned
:param frequency: options are daily,weekly,monthly,quarterly,annual
:param transformation: options are diff, rdiff, cumul, and normalize.
:param rows: Number of rows which will be returned.
:param returns: specify what format you wish your dataset returned as.
:returns Pandas Dataframe indexed by date.
"""
    #Lists of allowable parameters
    allowedfreq = ['daily', 'weekly', 'monthly', 'quarterly', 'annual']
    allowedtransform = ['rdiff','diff','cumul','normalize']
    allowedformats = ["pandas","numpy"]
    token = _getauthtoken(authtoken)
    #Basic API url
    url = 'http://www.quandl.com/api/v1/datasets/%s.csv?' % dataset
    #Deal with authorization token
    if token:
        url += 'auth_token=%s' % token
    #parse date parameters
    if startdate and not enddate:
        startdate = _parse_dates(startdate)
        url += '&trim_start=%s' % startdate
    elif startdate and enddate:
        startdate, enddate = _parse_dates(startdate), _parse_dates(enddate)
        url += '&trim_start=%s&trim_end=%s' % (startdate, enddate)
    #Check frequency parameter and append to call
    if frequency and frequency not in allowedfreq:
        error = 'Incorrect frequency specified. Use one of the following ' + ",".join(allowedfreq)
        raise Exception(error)
    elif frequency:
        url += '&collapse=%s' % frequency
    #Check if transformation is acceptable and append to api call
    if transformation and transformation not in allowedtransform:
        error = "Incorrect transformation given. Use one of the following" +",".join(allowedtransform)
        raise Exception(error)
    elif transformation:
        url += "&transformation=%s" % transformation
    #append row restriction to API call
    if rows:
        url +="&rows=%s" %rows
    #return data as numpy array if wished but checks first if it is an acceptable format to return.
    if returns not in allowedformats:
        error = "Incorrect format given. Use one of the following" +",".join(allowedformats)
        raise Exception(error)
     #Make the API call and download data as a CSV file to your python directory
    elif returns == 'pandas':
        urldata = _download(url)
        print 'Returning Dataframe for ', dataset
        return urldata
    elif returns == 'numpy':
        try:
            u=urllib2.urlopen(url)
            array = genfromtxt(u,names = True, delimiter=",",dtype=None)
            return array
        except urllib2.HTTPError as e:
            print 'url:',url
            raise Exception('Error Downloading, please check your parameters! %s' %e)


#Define helper function to parse dates
def _parse_dates(date):
    try:
        date = parser.parse(date)
    except ValueError:
        raise Exception('%s is not recognised a date' % date)
    return date.strftime('%Y-%m-%d')


#Helper function for actually making API call and downloading the file
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
