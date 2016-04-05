# 2.x Series package Notes

With the release of version 3 of our API we are officially deprecating version 2 of the `Quandl` python package. We have re-written the package from the ground up and will be moving forward with a 3.x.x package under the new namespace of `quandl` that will rely on version 3 of our RESTful API.

## Upgrading

There are numerous advantages to upgrade from the older 2.x series package including increased performance and stability. The upgrade process is fairly simple. 

1. Upgrade your package using pip. 

`pip install --upgrade quandl`

2. Wherever you have: 

```python
import Quandl
```

simply change this to: 

```python
import quandl as Quandl
```

3. Additionally if you were relying on a saved version of your `api key` _(authtoken)_ in your scripts please note that this functionality has been dropped from the existing package. To continue to load your api key from the filesystem we recommend you import the key and set it via the api config `quandl.ApiConfig.api_key`. Below is a example of importing your previously pickled key if it exists:

```python
import quandl as Quandl
import pickle
import os.path
if os.path.isfile('authtoken.p'):
    Quandl.ApiConfig.api_key = pickle.load(open('authtoken.p', 'rb'))
```

That's it! The new package should be ready to use.

## Continuing with the old release

If you wish to continue using the old package during this transitional period please follow the instructions below: 

https://github.com/quandl/quandl-python/tree/v2.8.9

To continue using Quandl API version 2, do the following:

1. Ensure you have [pip installed](https://pip.pypa.io/en/latest/installing.html)

2. In your python program's directory, execute `pip freeze > requirements.txt`. Alternatively, create the `requirements.txt` file and enter the desired Quandl package version, e.g., `Quandl==2.8.8`.

3. Execute `pip install -r requirements.txt` to ensure the desired Quandl package version is installed.


## FAQ

Q: `I tried out your sample code for loading the API key from a file and its not working.`
A: Note that for the sample code to work you must have access to read the file with the auth token. The sample script also assumes that file is stored in the same directory that the script is being run from. If you wish to use a key in another directory you will need to change the path to the key being used in the example.
