# 2.x Series package Notes

With the release of version 3 of our API we are officially deprecating version 2 of the Quandl Python package. We have re-written the package and will be moving forward with a 3.x.x package under the new namespace of `quandl` that will rely on version 3 of our RESTful API.

## Upgrading

There are numerous advantages to upgrade from the older 2.x series package including improved performance and stability. The upgrade process is fairly simple. 

Upgrade your package using pip and running: `pip install --upgrade quandl`

Wherever you have: 

```python
import Quandl
```

change this to: 

```python
import quandl as Quandl
```

Additionally if you were relying on a saved version of your `api key` _(authtoken)_ in your scripts please note that this functionality has been dropped from the existing package. To continue to load your api key from the filesystem we recommend you import the key and set it via the api config `quandl.ApiConfig.api_key`. Below is a example of importing your previously pickled key if it exists:

```python
import quandl as Quandl
import pickle
import os.path
if os.path.isfile('authtoken.p'):
    Quandl.ApiConfig.api_key = pickle.load(open('authtoken.p', 'rb'))
```

That's it! The new package should be ready to use.

## Continuing with the Old Release

If you wish to continue using the old package during this transitional period please follow the instructions below: 

https://github.com/quandl/quandl-python/tree/v2.8.9

To continue using Quandl API version 2, do the following:

1. Ensure you have [pip installed](https://pip.pypa.io/en/latest/installing.html)

2. In your Python program's directory, execute `pip freeze > requirements.txt`. Alternatively, create the `requirements.txt` file and enter the desired Quandl package version, e.g., `Quandl==2.8.9`.

3. Execute `pip install -r requirements.txt` to ensure the desired Quandl package version is installed.

Note: for the sample code to work you must have access to read the file with the auth token. The sample script also assumes that file is stored in the same directory from where the script is run. If you wish to use a key in another directory you will need to match the path used in the sample.
