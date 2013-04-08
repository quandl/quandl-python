import pandas as pd
import pickle
import urllib2
import urllib
import datetime
from dateutil import parser

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
        error = 'Incorrect frequency specified. Use one of the following, ' + ",".join(allowedfreq)
        raise Exception(error)
    elif frequency:
        url += '&collapse=%s' % frequency
        
    #Check if transformation is acceptable and append to api call
    if transformation and transformation not in allowedtransform:
        error = "Incorrect transformation given. Use one of the following, " +",".join(allowedtransform)
        raise Exception(error)
    elif transformation:
        url += "&transformation=%s" % transformation
        
    #append row restriction to API call
    if rows:
        url +="&rows=%s" %rows
        
    #return data as numpy array if wished but checks first if it is an acceptable format to return.
    if returns not in allowedformats:
        error = "Incorrect format given. Use one of the following, " +",".join(allowedformats)
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
        except IOError as e:
            print 'url:',url
            raise Exception("Parsing Error! %s" %e)        
        except urllib2.HTTPError as e:
            print 'url:',url
            raise Exception('Error Downloading! %s' %e)
        
        
        
#Upload your own datasets to Quandl        
def push(data, code, name, authtoken='', desc='', override = False):
    
    """Upload a dataset, a Pandas Dataframe object, to Quandl
    returns link to your dataset.
    
:param authtoken: Required to upload data
:param data: Required, pandas ts or numpy array
:param name: Dataset name, must consist of only capital letters, numbers, and underscores
:param desc: Description of dataset
:param overide: whether to overide dataset of same name
:returns link to uploaded data
"""    
    
    override = str(override).lower()
    token = _getauthtoken(authtoken)
    if token == '':
        error= "You need an API token to upload your data to Quandl, please see www.quandl.com/API for more"
        raise Exception(error)
    #check that code is correctly formated
    
    _pushcodetest(code)
    datestr=''
    
    #Format the data for upload.
    #check format of data
    #check if Pandas dataframe
    if isinstance(data,pd.core.frame.DataFrame):
        #check if indexed by date

        data_interm = data.to_records()
        index = data_interm.dtype.names
        datestr += ','.join(index) + '\n'
        
        for i in data_interm:
            if isinstance(i[0], datetime.datetime):
                datestr += i[0].date().isoformat()
            else:
                #Check if index is a date
                try :
                    datestr += _parse_dates(str(i[0]))
                except:
                    error=  "Please check your indices, one of them is not a recognizable date"
                    raise Exception(error)
            for n in i:
                if isinstance(n, float) or isinstance(n,int):
                    datestr += ',' + str(n)
            datestr += '\n'
    else:
        error = "only pandas data series are accepted for upload at this time"
        raise Exception(error)
    params = {'name':name,'code':code, 'description':desc,'update_or_create':override, 'data':datestr}    
            
    
    
    #create API URL
    url = "http://www.quandl.com/api/v1/datasets.json?auth_token=" + token 
    
    jsonreturn = _htmlpush(url,params)
    if jsonreturn["errors"] and jsonreturn["errors"]["code"][0] == "has already been taken":
        error = "You are trying to overwrite a dataset which already exists on Quandl. If this is what you wish to do please recall the function with overide = True"
        raise Exception(error)
    
    return "http://www.quandl.com/" + jsonreturn["source_code"] + "/" + jsonreturn["code"]



#Helper function to parse dates
def _parse_dates(date):
    #Check if datetime object
    if isinstance(date,datetime.datetime):
        return date.date().isoformat()
    if isinstance(date,datetime.date):
        return date.isoformat()
    try:
        date = parser.parse(date)
    except ValueError:
        raise Exception('%s is not recognised a date' % date)
    return date.date().isoformat()


#Helper function for actually making API call and downloading the file
def _download(url):
    try:
        dframe = pd.read_csv(url, index_col=0, parse_dates=True)
        return dframe
    except pd._parser.CParserError as e:
        print 'url:',url
        raise Exception('Error Reading Data! %s' %e)     
    except urllib2.HTTPError as e:
        print 'url:',url
        raise Exception('Error Downloading! %s' %e)
    
#Helper function to make html push
def _htmlpush(url,raw_params):
    page = url
    params = urllib.urlencode(raw_params)
    request = urllib2.Request(page, params)
    page = urllib2.urlopen(request)
    return json.loads(page.read())


def _pushcodetest(code):
    regex = re.compile('[^0-9A-Z_]')
    if not regex.search(code):
        return code
    else:
        error = "Your Quandl Code for uploaded data must consist of only capital letters, underscores and capital numbers."
        raise Exception(error)



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
        print "No authentication tokens found,usage will be limited"
        print "See www.quandl.com/api for more information"
    elif savedtoken and not token:
        token = savedtoken
        print 'Using cached token %s for authentication ' % token
    return token
