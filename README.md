Quandl API for Python
=========
See http://www.quandl.com/api

Basic wrapper to return datasets from the Quandl website as Pandas dataframe objects with a timeseries index.
This allows interactive manipulation of the results via IPython or storage of the datasets using Pandas I/O functions.
You will need a familarity with Pandas (http://pandas.pydata.org/) to get the most out of this.

Usage
=====
Usage is simple and mirrors the functionality found at http://www.quandl.com/api

A request with a full list of options would be the following.
import Quandl
data = Quandl.get('PRAGUESE/PX',authtoken='xxxxxx',startdate='2001-01-01',enddate='2010-01-01',frequency='annual')

All options beyond specifying the dataset (PRAUGESE/PX) are optional,though it is helpful to specify an authtoken at 
least once to increase download limits, it should be cached after that.

you can then view the dataframe with:
data.head()
See pandas tutorials for a wealth of options on data manipulation.

Authtokens are saved as pickled files in the local directory so it is unnecessary to enter them more than once,
unless you change your working directory.To replace simply save the new token or delete authtoken.p.

Recommended Usage
================
The IPython notebook is an excellent python environment for interactive data work.

I would suggest downloading the data in raw format in the highest frequency possible and preforming any data manipulation
in pandas itself. Dateranges and frequency have  been added to the api for the sake of completeness more than necessity.
See the following:http://pandas.pydata.org/pandas-docs/dev/timeseries.html


Dependencies
============
Pandas https://code.google.com/p/pandas/
dateutil (should be installed as part of pandas) http://labix.org/python-dateutil
