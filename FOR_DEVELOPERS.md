# Quandl Python detailed usage for Developers

Developer access gives more flexibility when making requests to the Quandl api. Although very similiar to the analyst method it allows for users to achieve unique lookups that cannot be done via the analyst api. These include:
 
* Retrieving metadata without data
* Customizing how data is returned more granularly
* Allowing easier iteration of data

## Retrieving Data

In the following sections, `params={}` represents optional query parameters that can be passed into each call. For more detail on available query parameters please see the [API Documentation](https://www.quandl.com/docs/api).

### Dataset

To retrieve a dataset's metadata use its full code:

```python
quandl.Dataset.get('WIKI/AAPL')
```

### Data

A dataset's data can be queried through the dataset object. For example:

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
data.to_csv()
=> "Id,Name,Database Code,Description,Datasets Count,Downloads,Premium,Image,Bundle Ids,Plan ...
```

To convert the data into a [pandas](http://pandas.pydata.org/) dataframe:

```python
data.to_pandas()
```

To convert the data into a [NumPy](http://www.numpy.org/) record:

```python
data.to_numpy()
```

Since the data is a [List](#list), the raw data can be retrieved via:

```python
data.to_list()
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
dataset = quandl.Dataset.get('WIKI/AAPL')
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

### Download Entire Database (Bulk Download)

To get the url for downloading all dataset data of a database:

```python
import quandl
quandl.ApiConfig.api_key = 'tEsTkEy123456789'
quandl.Database.get('ZEA').bulk_download_url()
=> "https://www.quandl.com/api/v3/databases/ZEA/data?api_key=tEsTkEy123456789"
```

To bulk download all dataset data of a database:

```python
quandl.ApiConfig.api_key = 'tEsTkEy123456789'
quandl.Database.get('ZEA').bulk_download_to_file('/path/to/destination/folder_or_file_path')
```

For bulk download of premium databases, please ensure that a valid `api_key` is set, as authentication is required.

For both `bulk_download_url` and `bulk_download_to_file`, an optional `download_type` query parameter can be passed in:

```python
quandl.Database.get('ZEA').bulk_download_to_file('.', params={'download_type': 'partial'})
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