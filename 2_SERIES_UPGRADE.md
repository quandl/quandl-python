# 2.x Series package Notes

With the release of our v3 API we are officially deprecating version 2 of the `Quandl` python package. We have re-written the package from the ground up and will be moving forward with a 3.x.x package under the new namespace of `quandl` that will rely on version 3 of our restful api.

## Upgrading

There are numerous advantages to upgrade from our older 2.x series package including increased performance and stability. The upgrade process is fairly simple. 

First upgrade your package using pip. ex: 

`pip install --upgrade quandl`

next wherever you have: 

```python
import Quandl
```

simply change this too: 

```python
import quandl as Quandl
```

Additionally if you were relying on a saved version of your `api key` _(authtoken)_ in your scripts please note that this functionality has been dropped from the existing package. To continue to load your api key from the filesystem we recommend you manually load the key and set it via the api config `quandl.ApiConfig.api_key`. Some example code that will do this is:

```python
import quandl as Quandl
import pickle
Quandl.ApiConfig.api_key = pickle.load(open('authtoken.p', 'rb'))
```

That's it! The new package should be ready to use.

## Continuing with the old release

If you wish to continue using the old package during this transitional period please follow the instructions below: 

https://github.com/quandl/quandl-python/tree/v2.8.9

To continue using quandl package version 2, do the following:

1. Ensure you have [pip installed](https://pip.pypa.io/en/latest/installing.html)

2. In your python program's directory, execute `pip freeze > requirements.txt`. Alternatively, create the `requirements.txt` file and enter the desired quandl package version, e.g., `Quandl==2.8.8` into it.

3. Execute `pip install -r requirements.txt` to ensure the desired quandl package version is installed


## FAQ

Q: `I tried out your sample code for loading the api key from a file and its not working.`
A: Note that for the sample code to work you must have access to read the file with the auth token. The sample script also assumes that file is stored in the same directory that the script is being run from. If you wish to use a key in another directory you will need to change the path being used in the example.