# Nasdaq Data Link Python Client
[![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiZUtvUFNYREloNE4vV0xWWEUxVS81S0toZjdQbzQrWXhQZ1BUbE1mZ1FMVXdSZXQ2K1ZLQ1ducmtqYTVWa2xBZXhRMWVGemVKWitzVm5MNXI4cGZYb21RPSIsIml2UGFyYW1ldGVyU3BlYyI6Im0vdUljcjBjdmpGVU9XdXUiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)]()
[![PyPI version](https://badge.fury.io/py/Quandl.svg)](https://badge.fury.io/py/Quandl)

This is the official documentation for Nasdaq Data Link's Python Package. The package can be used to interact with the latest version of the [Nasdaq Data Link's RESTful API](https://docs.data.nasdaq.com/docs). This package is compatible with python v2.7.x and v3.x+.

## Installation

The installation process varies depending on your python version and system used. However in most cases the following should work:

```shell
pip install nasdaq-data-link
```

Alternatively on some systems python3 may use a different pip executable and may need to be installed via an alternate pip command. For example:

```shell
pip3 install nasdaq-data-link
```

## Configuration

| Option | Explanation | Example |
|---|---|---|
| api_key | Your access key | `tEsTkEy123456789` | Used to identify who you are and provide full access. |
| use_retries | Whether API calls which return statuses in `retry_status_codes` should be automatically retried | True
| number_of_retries | Maximum number of retries that should be attempted. Only used if `use_retries` is True | 5
| max_wait_between_retries | Maximum amount of time in seconds that should be waited before attempting a retry. Only used if `use_retries` is True | 8
| retry_backoff_factor | Determines the amount of time in seconds that should be waited before attempting another retry. Note that this factor is exponential so a `retry_backoff_factor` of 0.5 will cause waits of [0.5, 1, 2, 4, etc]. Only used if `use_retries` is True | 0.5
| retry_status_codes | A list of HTTP status codes which will trigger a retry to occur. Only used if `use_retries` is True| [429, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511]

```python
import nasdaqdatalink
nasdaqdatalink.ApiConfig.api_key = 'tEsTkEy123456789'
```
By default, SSL verification is enabled. To bypass SSL verification
```python
nasdaqdatalink.ApiConfig.verify_ssl = False
```

### Local API Key file
Save local key to `$HOME/.nasdaq_data_link_api_key` file
```
import nasdaqdatalink
nasdaqdatalink.save_key("supersecret")
print(nasdaqdatalink.ApiConfig.api_key)
```

Load the API Key without exposing the key in the script or notebook
```
import nasdaqdatalink
nasdaqdatalink.read_key()
print(nasdaqdatalink.ApiConfig.api_key)
```

Set a custom location for the API key file, e.g. store the externally outside a docker container
```
import nasdaqdatalink
nasdaqdatalink.save_key("ourcorporateapikey", filename="/srv/data/somecontainer/.corporatenasdaqdatalinkapikey")
```
and call within the docker container with mount point at `/data`
```
import nasdaqdatalink
nasdaqdatalink.read_key(filepath="/data/.corporatenasdaqdatalinkapikey")
```


## Retrieving Data

There are two methods for retrieving data in Python: the Quick method and the Detailed method. The latter is more suitable to application programming. Both methods work with Nasdaq Data Link's two types of data structures: time-series (dataset) data and non-time series (datatable).

The following quick call can be used to retrieve a dataset:

```python
import nasdaqdatalink
data = nasdaqdatalink.get('NSE/OIL')
```

This example finds all data points for the dataset `NSE/OIL` and stores them in a pandas dataframe. You can then view the dataframe with data.head().

A similar quick call can be used to retrieve a datatable:

```python
import nasdaqdatalink
data = nasdaqdatalink.get_table('ZACKS/FC', ticker='AAPL')
```

This example retrieves all rows for `ZACKS/FC` where `ticker='AAPL'` and stores them in a pandas dataframe. Similarly you can then view the dataframe with data.head().

Note that in both examples if an `api_key` has not been set you may receive limited or sample data. You can find more details on these quick calls and others in our [Quick Method Guide](./FOR_ANALYSTS.md).

### Logging

Currently, Nasdaq Data Link debug logging is limited in scope.  However, to enable debug
logs you can use the following snippet.

```python
import nasdaqdatalink
import logging

logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)  # optionally set level for
everything.  Useful to see dependency debug info as well.

data_link_log = logging.getLogger("nasdaqdatalink")
data_link_log.setLevel(logging.DEBUG)
```


### Detailed Usage

Our API can provide more than just data. It can also be used to search and provide metadata or to programmatically retrieve data. For these more advanced techniques please follow our [Detailed Method Guide](./FOR_DEVELOPERS.md).

## Local Development

### Setup

If you wish to work on local development please clone/fork the git repo and use `pip install -r requirements.txt` to setup the project.

### Testing

We recommend the following tools for testing any changes:

* [nose](https://nose.readthedocs.org/en/latest/) for running tests.
* [tox](https://pypi.python.org/pypi/tox) for testing against multiple versions of python.
* [flake8](https://flake8.readthedocs.org/en/latest/) for syntax checking.
* [virtualenv](https://virtualenv.pypa.io/en/latest/) for use with tox virtualization.

The following are instructions for running our tests:

1. Make sure a version of python 2.7 or python 3.x is installed locally in your system. To avoid permission issues on OSX we recommend installing the packages from: https://www.python.org/downloads/
2. Install `virtualenv` and `tox` using:
    `pip install tox virtualenv`
3. Run following command (you may notice slow performance the first time):
    `python setup.py install`
4. Run the following command to test the plugin in all versions of python we support:
    `tox`

Once you have all required packages installed, you can run tests locally with:

Running all tests locally

```python
python -W always setup.py -q test
```

Running an individual test

```python
python -m unittest test.[test file name].[class name].[individual test name]`
```

Example:

```python
python -m unittest -v test.test_datatable.ExportDataTableTest.test_download_get_file_info
```

## Recommended Usage

We would suggest downloading the data in raw format in the highest frequency possible and performing any data manipulation
in pandas itself.

See [this link](http://pandas.pydata.org/pandas-docs/dev/timeseries.html) for more information about timeseries in pandas.

## Release the Package

To release the package, you can follow the instructions on this [page](https://packaging.python.org/tutorials/packaging-projects/#packaging-python-projects)

## Additional Links

* [Nasdaq Data Link](https://data.nasdaq.com)
* [Nasdaq Data Link Tools](https://data.nasdaq.com/tools/full-list)
* [API Docs](https://docs.data.nasdaq.com/docs)

## License

[MIT License](http://opensource.org/licenses/MIT)
