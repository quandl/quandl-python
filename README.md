Quandl API for Python
=====================
Basic wrapper to return datasets from the Quandl website as Pandas DataFrame objects with a timeseries index, or as a numpy array. This allows interactive manipulation of the results via IPython or storage of the datasets using Pandas I/O functions. You will need a familarity with [pandas](http://pandas.pydata.org/) to get the most out of this.

Usage
=====

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

Authtokens are sav
ed as pickled files in the local directory so it is unnecessary to enter them more than once,
unless you change your working directory. To replace simply save the new token or delete the `authtoken.p` file.



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


### Download Multiple Codes


If you wanted to compare the closing prices for Apple and Microsoft, you would obtain the two Quandl codes:

`GOOG/NASDAQ_AAPL`

`GOOG/NASDAQ_MSFT`

Append the column you wish to get with a `.`, and put them into an array.

`['GOOG/NASDAQ_AAPL.4','GOOG/NASDAQ_MSFT.4']`

Just make a normal get call with the array passed to get, and your multiset will be returned.

`data= Quandl.get(['GOOG/NASDAQ_AAPL.4','GOOG/NASDAQ_MSFT.4'])`

Which outputs:

```
No authentication tokens found: usage will be limited.
See www.quandl.com/api for more information.
Returning Dataframe for  [u'GOOG.NASDAQ_AAPL.4', u'GOOG.NASDAQ_MSFT.4']

        GOOG.NASDAQ_AAPL - Close  GOOG.NASDAQ_MSFT - Close
Date                                                          
1997-08-20        6.16                     17.57
1997-08-21        6.00                     17.23
1997-08-22        5.91                     17.16
1997-08-25        5.77                     17.06
1997-08-26        5.56                     16.88

```


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
