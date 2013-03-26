Quandl API for Python
=========
See http://www.quandl.com/api

Basic wrapper to return datasets from the Quandl website as Pandas dataframe objects with a timeseries index.
This allows interactive manipulation of the results via IPython or storage of the datasets using Pandas I/O functions.
You will need a familarity with Pandas (http://pandas.pydata.org/) to get the most out of this.

Example
========
An example of creating a pandas time series for S&P 500 data, with a weekly frequency

    import Quandl
    data = Quandl.get("YAHOO/INDEX_GSPC",frequency="weekly")
    data.head()
will output

    No authentication tokens found,usage will be limited 
    Returning Dataframe for  YAHOO/INDEX_GSPC
               Open     High      Low    Close      Volume  Adjusted Close
    Date                                                                      
    2013-03-25  1556.89  1564.91  1546.22  1551.69  3178170000         1551.69
    2013-03-15  1563.21  1563.62  1555.74  1560.70  5175850000         1560.70
    2013-03-08  1544.26  1552.48  1542.94  1551.18  3652260000         1551.18
    2013-03-01  1514.68  1519.99  1501.48  1518.20  3695610000         1518.20
    2013-02-22  1502.42  1515.64  1502.42  1515.60  3419320000         1515.60

Usage
=====
Usage is simple and mirrors the functionality found at http://www.quandl.com/api

A request with a full list of options would be the following.
```
import Quandl
data = Quandl.get('PRAGUESE/PX',authtoken='xxxxxx',startdate='2001-01-01',enddate='2010-01-01',frequency='annual',transformation = 'rdiff',rows='4',formats='numpy')
```
All options beyond specifying the dataset (PRAUGESE/PX) are optional,though it is helpful to specify an authtoken at 
least once to increase download limits, it should be cached after that.

you can then view the dataframe with:
```
data.head()
```

See the pandas documentation for a wealth of options on data manipulation.

Authtokens are saved as pickled files in the local directory so it is unnecessary to enter them more than once,
unless you change your working directory.To replace simply save the new token or delete authtoken.p.


Recommended Usage
================
The IPython notebook is an excellent python environment for interactive data work. Spyder is also a superb IDE for analysis and more numerical work.

I would suggest downloading the data in raw format in the highest frequency possible and preforming any data manipulation
in pandas itself.
See the following:http://pandas.pydata.org/pandas-docs/dev/timeseries.html

Questions/Comments
==================
Please send any questions, comments, or any other inquires about this package to Chris@quandl.com


Dependencies
============
Pandas https://code.google.com/p/pandas/

dateutil (should be installed as part of pandas) http://labix.org/python-dateutil
