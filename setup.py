try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import Quandl

setup(name = 'Quandl',
      description = 'Package for Quandl API access',
      version = Quandl.__version__,
      author = ", ".join(Quandl.__authors__),
      maintainer = Quandl.__maintainer__,
      maintainer_email = Quandl.__email__,
      url = Quandl.__url__,
      license = Quandl.__license__,
      install_requires = [
      "pandas >= 0.14",
      "numpy >= 1.8",
      ],
      packages = ['Quandl'],
)
