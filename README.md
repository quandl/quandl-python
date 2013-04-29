Quandl API for Python
=====================
Basic wrapper to return datasets from the Quandl website as Pandas dataframe objects with a timeseries index, or as a numpy array. This allows interactive manipulation of the results via IPython or storage of the datasets using Pandas I/O functions. You will need a familarity with [pandas](http://pandas.pydata.org/) to get the most out of this.

See the [Quandl API](http://www.quandl.com/api) for more information.


Usage
=====
Usage is simple and mirrors the functionality found at [Quandl/API](http://www.quandl.com/api).

A request with a full list of options would be the following.

```python
data = Quandl.get('PRAGUESE/PX', authtoken='xxxxxx', trim_start='2001-01-01',
                  trim_end='2010-01-01', collapse='annual',
                  transformation='rdiff', rows=4, returns='numpy')
```

All options beyond specifying the dataset (PRAUGESE/PX) are optional,though it is helpful to specify an authtoken at 
least once to increase download limits.

You can then view the dataframe with `data.head()`.

See the [pandas documentation](http://pandas.pydata.org/) for a wealth of options on data manipulation.

Authtokens are saved as pickled files in the local directory so it is unnecessary to enter them more than once,
unless you change your working directory. To replace simply save the new token or delete the `authtoken.p` file.


## Search Example
An example of searching for datasets having to do with oil: 

```python
import Quandl
datasets = Quandl.search('OIL')
datasets[0]
```

will output 

```python
{u'code': u'OIL',
 u'created_at': u'2011-11-07T19:39:22Z',
 u'description': u'Historical prices for Oil India Limited (OIL),
                   (ISIN: INE274J01014),  National Stock Exchange of India.',
 u'frequency': u'daily',
 u'from_date': u'2009-09-30',
 
 [... elided ...]

 u'highlights': {u'description': u'Historical prices for <em>Oil</em> India
                                   Limited (<em>OIL</em>), (ISIN: INE274J01014),
                                   National Stock Exchange of India.',
 u'name': u'<em>Oil</em> India Limited'},
 u'import_url': u'http://www.nseindia.com/[...]'
 u'keywords': u'Finance,India,Stocks,NSE'}
```


## Get Example
An example of creating a pandas time series for IBM stock data, with a weekly frequency:

```python
data = Quandl.get('GOOG/NYSE_IBM', collapse='weekly')
data.head()
```

will output

```
No authentication tokens found,usage will be limited
Returning Dataframe for  GOOG/NYSE_IBM

              Open    High     Low   Close   Volume
Date
2013-03-28  209.83  213.44  209.74  213.30  3752999
2013-03-15  215.38  215.90  213.41  214.92  7937244
2013-03-08  209.85  210.74  209.43  210.38  3700986
2013-03-01  200.65  202.94  199.36  202.91  3309434
2013-02-22  199.23  201.09  198.84  201.09  3107976
```


## Push Example
You can now upload your own data to Quandl through the Python package.

At this time the only accepted format is a date indexed Pandas DataSeries.

Things to do before you upload:

* Make an account and set your authentication token within the package with the Quandl.auth() function.
* Get your data into a data frame with the dates in the first column.
* Pick a code for your dataset - only capital letters, numbers and underscores are acceptable.

Then call the following to push the data:

```python
Quandl.push(data, code='TEST', name='Test', desc='test')
```

All parameters but desc are necessary

If you wish to override the existing set at code `TEST` add `override=True`.

Uploading a pandas DataSeries with random data:

```python
import pandas
import numpy

index = ['Dec 12 2296', 'Dec 21 1998', 'Oct 9 2000', 'Oct 19 2001',
         'Oct 30 2003', 'Nov 12 2003']
data = pandas.DataFrame(numpy.random.randn(6, 3), index=index,
                        columns=['D', 'B', 'C'])
print Quandl.push(data, code='F32C', name='Test', desc='test',
                  authtoken='xxxxxx')
```

Will print the link to your newly uploaded data.


Recommended Usage
================
The IPython notebook is an excellent python environment for interactive data work. Spyder is also a superb IDE for analysis and more numerical work.

I would suggest downloading the data in raw format in the highest frequency possible and preforming any data manipulation
in pandas itself.

See [this link](http://pandas.pydata.org/pandas-docs/dev/timeseries.html) for more information about timeseries in pandas.


Questions/Comments
==================
Please send any questions, comments, or any other inquires about this package to <Chris@quandl.com>.


Installation
============
The stable version of Quandl can be installed with pip:

    pip install Quandl


Dependencies
============
Pandas :: <https://code.google.com/p/pandas/>

dateutil (should be installed as part of pandas) :: <http://labix.org/python-dateutil>


License
=======
[MIT License](http://opensource.org/licenses/MIT)

