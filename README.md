# Quandl Python Client [![Build Status](https://travis-ci.org/quandl/quandl-python.svg?branch=master)](https://travis-ci.org/quandl/quandl-python)

The official python package for all your data needs. The Quandl client can be used to interact with the latest version of the [Quandl RESTful API](https://www.quandl.com/docs/api). This package is compatible with python v2.7.x and v3.x+

## Deprecation of old package

Please see this readme for more information and upgrade instructions: [2.x series transition notes](./2_SERIES_UPGRADE.md)

## Installation

The installation process varies depending on your python version and system used. However in most cases the following should work:

```shell
pip install quandl
```

Alternatively on some systems python3 may use a different pip executable and may need to be installed via an alternate pip command. ex:

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

`quandl.ApiConfig.api_version` is optional however it is strongly recommended that is provided to avoid issues with rate-limiting. For premium databases, datasets and datatables `quandl.ApiConfig.api_key` will need to be set to identify you to our api. Please see [API Documentation](https://www.quandl.com/docs/api) for more detail.

## Retrieving Data

Retrieving data can be done easily using the analyst convenience methods. The following call can be used to retrieve dataset data:

```python
import quandl
data = quandl.get('NSE/OIL')
```

The previous example will find all data points for the dataset `NSE/OIL` and stores them in a pandas dataframe. You can then view the dataframe with data.head().

A similiar call can be used to retrieve a database datatable:

```python
import quandl
data = quandl.get_table('ZACKS/FC', ticker='AAPL')
```

This example retrieves all rows for `ZACKS/FC` where `ticker='AAPL'` and stores them in a pandas dataframe. Similarily you can then view the dataframe with data.head().

Note that in both example if an `api_key` has not bee set you may recieved limited or example data. Note that unlike Datasets, Datatables will return a preview sample of data if you do not use an api_key with access to the data. You can find more details on these call and others like it in our [Detailed guide for analysts](./FOR_ANALYSTS.md)

### Additional Usages

Our api can provide more than just data. It can also be used to search and provide metadata or to programatically retrieve data. For these more advanced techniques please follow our [Detailed guide for developers](./FOR_DEVELOPERS.md)

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
2. Be sure to install `virtualenv` and `tox` are installed
    `pip install tox virtualenv`
3. Run following commands, it may be slow for the very first time as dependencies are setup:
    `python setup.py install`
4. Run the following command to test the plugin in all versions of python we support:
    `tox`

## Recommended Usage

We would suggest downloading the data in raw format in the highest frequency possible and preforming any data manipulation
in pandas itself.

See [this link](http://pandas.pydata.org/pandas-docs/dev/timeseries.html) for more information about timeseries in pandas.

## Questions/Comments

For any questions, comments or inquires about this package please open a ticket on the github repo or email the development team at <dev@quandl.com>. For any questions about data provided by the API please email connect@quandl.com

## Additional Links

* [Quandl](https://www.quandl.com)
* [Quandl Tools](https://www.quandl.com/tools/api)
* [API Docs](https://www.quandl.com/docs/api)

## License

[MIT License](http://opensource.org/licenses/MIT)
