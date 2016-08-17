# Quick Method Guide - Quandl-Python

This quick guide offers convenient ways to retrieve individual datasets or datatables with the Python package without the need for complex commands.  

## Retrieving Data

Retrieving data can be achieved easily using the two methods `quandl.get` for datasets and `quandl.get_table` for datatables. In both cases we strongly recommend that you set your api key via:

 ```python
import quandl
quandl.ApiConfig.api_key = 'tEsTkEy123456789'
```

### Datasets

To retrieve a Quandl dataset you can make the following call:

```python
import quandl
data = quandl.get('NSE/OIL')
```

This finds all data points for the dataset `NSE/OIL` and stores them in a pandas dataframe. You can then view the dataframe with:

```python
data.head()
```

However we recommend applying filters to streamline the results. To do this you may want to specify some additional filters and transformations.

```python
import quandl
data = quandl.get('NSE/OIL', start_date='2010-01-01', end_date='2014-01-01',
                  collapse='annual', transformation='rdiff',
                  rows=4)
```

This revised query will find all data points annually for the dataset `NSE/OIL` between the year 2010 and 2014 and transform them using the `rdiff` transformation. The query parameters used are documented in our [api docs](https://www.quandl.com/docs/api#data). Since the `data` was retrieved in the pandas format you can then view the dataframe with data.head().

#### Available parameters:

The following additional parameters can be specified for a dataset call:

| Option | Explanation | Example | Description |
|---|---|---|---|
| api_key | Your access key | `api_key='tEsTkEy123456789'` | Used to identify who you are and provide more access. Only required if not set via `quandl.ApiConfig.api_key=` |
| \<filter / transformation parameter\> | A parameter which filters or transforms the resulting data | `start_date='2010-01-01` | For a full list see our [api docs](https://www.quandl.com/docs/api#data) |

For more information on how to use and manipulate the resulting data see the [pandas documentation](http://pandas.pydata.org/).

#### Download Entire Database (Bulk Download)

You can download all the data in a database in a single call. The following will download the entire EOD database as a zip file to your current working directory:

```python
import quandl
quandl.bulkdownload('EOD')
```

After the download is finished, the `quandl.bulkdownload` will return the filename of the downloaded zip file. 

To download database data from the previous day, use the download_type option:

```python
import quandl
quandl.bulkdownload('EOD', download_type='partial')
```

You can also change the filename of the downloaded zip file by using the filename option:

```python
import quandl
quandl.bulkdownload('EOD', filename='/my/path/EOD_DB.zip')
```

#### Download Multiple Codes

Sometimes you want to compare two codes. For example if you wanted to compare the closing prices for Apple and Microsoft, you would obtain the two Quandl codes:

`WIKI/AAPL` vs. `WIKI/MSFT`

Append the column you wish to get with a `.`, and put them into an array.

`['WIKI/AAPL.11','WIKI/MSFT.11']`

Just make a normal get call with the array passed to get, and your multiset will be returned.

#### Download Multiple Codes (Multiset)

If you want to get multiple codes at once, delimit the codes with ',', and put them into an array. This will return a multiset.

For example:
```python
data = quandl.get(['WIKI/AAPL.11','WIKI/MSFT.11'])
```

Which outputs:

```
See www.quandl.com/docs/api for more information.
Returning Dataframe for  ['WIKI.AAPL.11', 'WIKI.MSFT.11']

        WIKI.AAPL - Close  WIKI.MSFT - Close
Date                                                          
1997-08-20        6.16                     17.57
1997-08-21        6.00                     17.23
1997-08-22        5.91                     17.16
1997-08-25        5.77                     17.06
1997-08-26        5.56                     16.88

```

### Datatables

Datatables work similarly to datasets but provide more flexibility when it comes to filtering. For example a simple way to retrieve datatable information would be:

```python
import quandl
data = quandl.get_table('ZACKS/FC')
```

Given the volume of data stored in datatables, this call will retrieve the first page of the `ZACKS/FC` datatable. You may turn on pagination to return more data by using:

```python
import quandl
data = quandl.get_table('ZACKS/FC', paginate=True)
```

This will retrieve multiple pages of data and merge them together as if they were one large page. In some cases, however, you will still exceed the request limit. In this case we recommend you filter your data using the available query parameters, as in the following example:

```python
import quandl
data = quandl.get_table('ZACKS/FC', paginate=True, ticker=['AAPL', 'MSFT'], per_end_date={'gte': '2015-01-01'}, qopts={'columns':['ticker', 'per_end_date']})
```

In this query we are asking for more pages of data, `ticker` values of either `AAPL` or `MSFT` and a `per_end_date` that is greater than or equal to `2015-01-01`. We are also filtering the returned columns on `ticker`, `per_end_date` and `comp_name` rather than all available columns. The output format is `pandas`.

#### Available parameters:

The following additional parameters can be specified for a datatable call:

| Option | Explanation | Example | Description |
|---|---|---|---|
| api_key | Your access key | `api_key='tEsTkEy123456789'` | Used to identify who you are and provide more access. Only required if not set via `quandl.ApiConfig.api_key=` |
| \<filter / transformation parameter\> | A parameter which filters or transforms the resulting data | `start_date='2010-01-01'` | For a full list see our [api docs](https://www.quandl.com/docs/api#datatables) |
| paginate | Wether to autoamtically paginate data | `paginate=True` | Will paginate through the first few pages of data automatically and merge them together in a larger output format. |

For more information on how to use and manipulate the resulting data see the [pandas documentation](http://pandas.pydata.org/).

#### Things to note

* Some datatables will return `sample` data if a valid api key is not used. If you are not receiving all of the expected data please double check your API key.
* When using the paginate=True option depending on the total number of rows in the result set you may receive an error indicating that there are more pages that have not been downloaded. This is due to a very large result sets that would be too large to send via the analyst method. If this happens we recommend you take one of two approaches:
  * *(recommended)* Refine your filter parameters to retrieve a smaller results set
  * Use the the [Detailed](./FOR_DEVELOPERS.md) method to iterate through more of the data.

## More usages

For even more advanced usage please see our [Detailed Method Guide] (./FOR_DEVELOPERS.md).
