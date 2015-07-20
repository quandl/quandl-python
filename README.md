# Quandl Python Client [![Build Status](https://travis-ci.org/quandl/quandl-python.svg?branch=master)](https://travis-ci.org/quandl/quandl-python)

The official python package for all your data needs! The Quandl client can be used to interact with the latest version of the [Quandl RESTful API](https://www.quandl.com/docs/api). This package is compatible with python v2.7.x and v3.4.x+

## Deprecation of old package

With the release of our v3 API we are officially deprecating version 2 of the `Quandl` python package. We have re-written the package from the ground up and will be moving forward with a 3.x.x package under the new namespace of `quandl` that will rely on version 3 of our restful api. During this transitional period you can continue to use the old package here: 

https://github.com/quandl/quandl-python/tree/v2.8.7

To continue using quandl package version 2, do the following:

1. Ensure you have [pip installed](https://pip.pypa.io/en/latest/installing.html)

2. In your python program's directory, execute `pip freeze > requirements.txt`. Alternatively, create the `requirements.txt` file and enter the desired quandl package version, e.g., `Quandl==2.8.8` into it.

3. Execute `pip install -r requirements.txt` to ensure the desired quandl package version is installed

## Installation

Installation varies depending on python version and system used. However in most cases the following should work:

```shell
pip install quandl
```

Alternatively on some systems python3 may use a different pip executable and may need to be installed via:

```shell
pip3 install quandl
```

## Configuration

| Option | Explanation | Example |
|---|---|---|
| api_key | Your access key | `tEsTkEy123456789` | Used to identify who you are and provide more access. |
| api_version | The version you wish to access the api with | 2015-04-09 | Can be used to test your code against the latest version without committing to it. |

```python
import quandl
quandl.ApiConfig.api_key = 'tEsTkEy123456789'
quandl.ApiConfig.api_version = '2015-04-09'
```

`quandl.ApiConfig.api_version` is optional (Please see [API Documentation](https://www.quandl.com/docs/api) for more detail). For non-premium datatabases/datasets, `quandl.ApiConfig.api_key` does not need to be set. It is useful to set your API key to increase your daily limits.

## Retrieving Data

In the following sections, `params={}` represents optional query parameters that can be passed into each call. For more detail on query parameters please see the [API Documentation](https://www.quandl.com/docs/api).

### Dataset

To retrieve a dataset use its full code:

```python
quandl.Dataset.get('WIKI/AAPL')
```

### Data

Dataset data can be queried through a dataset. For example:

```python
data = quandl.Dataset.get('WIKI/AAPL').data()
```

A number of optional query parameters can be passed to `data()`:

```python
dataset_data = quandl.Dataset.get('WIKI/AAPL').data(params={ 'start_date':'2001-01-01', 'end_date':'2010-01-01', 'collapse':'annual', 'transformation':'rdiff', 'rows':4 })
```

You can access the data much like you would other lists. In addition all the data column fields are mapped to their column_names for convenience:

```python
dataset_data[0].date
```

### Data formats

To convert the data into csv format:

```python
dataset_data.to_csv()
=> "Id,Name,Database Code,Description,Datasets Count,Downloads,Premium,Image,Bundle Ids,Plan ...
```

To convert the data into a [pandas](http://pandas.pydata.org/) dataframe:

```python
dataset_data.to_pandas()
```

To convert the data into a [NumPy](http://www.numpy.org/) record:

```python
dataset_data.to_numpy()
```

Since the data is a [List](#list), the raw data can be retrieved via:

```python
dataset_data.to_list()
```

All options beyond specifying the dataset `WIKI/AAPL` are optional.

See the `pandas` and `NumPy` documentation for a wealth of options on data manipulation.


### Database

To retrieve a database simply use its code with the get parameter:

```python
import quandl
quandl.Database.get('WIKI')
```

```python
dataset = quandl.Dataset.get(''WIKI/AAPL')
dataset.database()
```

You can also retrieve a list of databases by using:

```python
quandl.Database.all()
```

By default, each list query will return page 1 of the first 100 results (please see the official [API Documentation](https://www.quandl.com/docs/api) for more detail).

You can also retrieve the dataset through the database by using the helper method.

```python
quandl.Database.get('WIKI').datasets()
```

### Database Bulk Download

To get the url for bulk download of all datasets data of a database:

```python
import quandl
quandl.ApiConfig.api_key = 'tEsTkEy123456789'
quandl.Database.get('ZEA').bulk_download_url()
=> "https://www.quandl.com/api/v3/databases/ZEA/data?api_key=tEsTkEy123456789"
```

To bulk download all datasets data of a database:

```python
quandl.ApiConfig.api_key = 'tEsTkEy123456789'
quandl.Database.get('ZEA').bulk_download_to_file('/path/to/destination/folder')
```

For bulk download of premium databases, please ensure that a valid `api_key` is set, as authentication is required.

For both `bulk_download_url` and `bulk_download_to_file`, an optional `download_type` parameter can be passed in:

```python
quandl.Database.get('ZEA').bulk_download_to_file('.', download_type='partial')
```

If `download_type` is not specified, a `complete` bulk download will be performed. Please see the [API Documentation](https://www.quandl.com/docs/api) for more detail.

### MergedDataset

You can get a merged representation of multiple datasets.

```python
import quandl
merged_dataset = quandl.MergedDataset.get([('GOOG/NASDAQ_AAPL', {'column_index': [4]}),
                                           ('GOOG/NASDAQ_MSFT', {'column_index': [1,4]}), 'GOOG/NYSE_TWTR'])
```

In the above example the following data will be merged together:

* column 4 of dataset 'GOOG/NASDAQ_AAPL'
* columns 1 and 4 of dataset 'GOOG/NASDAQ_MSFT'
* all columns of 'GOOG/NYSE_TWTR' is requested

To get the data for the MergedDataset:

```python
data = merged_dataset.data()
```

The same optional query parameters shown in [Dataset data](#data) can be passed to `data()`

`data` represents a full outer join of data from the requested datasets. `data` can also be converted to csv, pandas, and NumPy in exactly the same way as [Dataset data](#data-formats)


## Working with results

### Instance

All data once retrieved is abstracted into custom classes. You can get a list of the fields in each class by using the `data_fields` method.

```python
import quandl
database = quandl.Database.get('WIKI')
database.data_fields()
=> ['name', 'downloads', 'id', 'premium', 'description', 'datasets_count', 'database_code', 'image']
```

You can then uses these methods in your code. Additionally you can access the data by using the hash equalivalent lookup.

```python
database = quandl.Database.get('WIKI')
database.database_code
=> 'WIKI'
database['database_code']
=> 'WIKI'
```

In some cases name of the fields returned by the API may not be compatible with the python language syntax. These will be converted into compatible field names.

```python
data = quandl.Dataset.get('WIKI/AAPL').data(params={ 'limit': 1 })[0]

data.column_names
=> ["Date", "Open", "High", "Low", "Close", "Volume", "Ex-Dividend", "Split Ratio", "Adj. Open", "Adj. High", "Adj. Low", "Adj. Close", "Adj. Volume"]

data.data_fields()
=> ["date", "open", "high", "low", "close", "volume", "ex_dividend", "split_ratio", "adj_open", "adj_high", "adj_low", "adj_close", "adj_volume"]
```

### List

All list queries will return an object inherited from ModelList.

To get the values of a list:

```python
import quandl
databases = quandl.Database.all()
databases.values
```

To get the metadata of a list:

```python
databases = quandl.Database.all()
databases.meta
```

To get the raw data of a list:

```python
databases = quandl.Database.all()
databases.to_list()
```

`Database.all()` and `Dataset.all()` will return a paginated list of results in the form of a PaginatedList object. You can check whether the PaginatedList has more data by using the `has_more_results()` method. By default, each list query will return page 1 of the first 100 results (please see the official [API Documentation](https://www.quandl.com/docs/api) for more detail). Depending on the list query results, you can pass additional parameters to filter the data:

```python
databases = quandl.Database.all()
=> ... results ...
databases.has_more_results()
=> true
quandl.Database.all(params={ 'page': 2 })
=> ... more results ...
```

Lists also function as arrays and can be iterated through. Note however that using these features will only work on the current page of data you have locally. You will need to continue to fetch results and iterate again to loop through the full result set.

```python
databases = quandl.Database.all()
for database in databases:
    print(database.database_code)
=> ... print database codes ...
databases.has_more_results()
=> true
more_databases = quandl.Database.all(params={ 'page': 2 })
for database in more_databases:
    print(database.database_code)
=> ... print more database codes ...
```

Lists also return metadata associated with the request. This can include things like the current page, total results, etc. Each of these fields can be accessed through a hash or convenience method.

```python
quandl.Database.all().current_page
=> 1
quandl.Database.all()['current_page']
=> 1
```

## Testing

1. Make sure python 2.7 and python 3.4 is installed locally in your system. To avoid permission issues on OSX we recommend installing the packages from: https://www.python.org/downloads/
2. Be sure to install `virtualenv` and `tox` are installed
    `pip install tox virtualenv`
3. Run following commands, it may be slow for the very first time
    `python setup.py install`
    `python3 setup.py install`
4. Run the command for testing in python 2.7 and python 3.4
    `tox`

## Recommended Usage

The IPython notebook is an excellent python environment for interactive data work. Spyder is also a superb IDE for analysis and more numerical work.

We would suggest downloading the data in raw format in the highest frequency possible and preforming any data manipulation
in pandas itself.

See [this link](http://pandas.pydata.org/pandas-docs/dev/timeseries.html) for more information about timeseries in pandas.

## Questions/Comments

For any questions, comments or inquires about this package please open a ticket on the github repo or email the development team at <dev@quandl.com>. For any questions about data provided by the API please email connect@quandl.com

## Dependencies

For the latest dependencies please reference `install_requires` in this file: https://github.com/quandl/quandl-python/blob/master/setup.py

## Additional Links

* [Quandl](https://www.quandl.com)
* [Quandl Tools](https://www.quandl.com/tools/api)
* [API Docs](https://www.quandl.com/docs/api)

## License

[MIT License](http://opensource.org/licenses/MIT)
