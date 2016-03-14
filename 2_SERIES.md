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

That's it! The new package should be ready to use.

## Continuing with the old release

If you wish to continue using the old package during this transitional period please follow the instructions below: 

https://github.com/quandl/quandl-python/tree/v2.8.9

To continue using quandl package version 2, do the following:

1. Ensure you have [pip installed](https://pip.pypa.io/en/latest/installing.html)

2. In your python program's directory, execute `pip freeze > requirements.txt`. Alternatively, create the `requirements.txt` file and enter the desired quandl package version, e.g., `Quandl==2.8.8` into it.

3. Execute `pip install -r requirements.txt` to ensure the desired quandl package version is installed
