import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('LONG_DESCRIPTION.rst') as f:
    long_description = f.read()

# Don't import quandl module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'quandl'))
# can only import VERSION successfully after the above line
# ignore flake8 warning that requires imports to be at the top
from version import VERSION  # NOQA

install_requires = [
    'pandas >= 0.14',
    'numpy >= 1.8',
    'requests >= 2.7.0',
    'inflection >= 0.3.1',
    'python-dateutil',
    'six',
    'more-itertools'
]

installs_for_two = [
    'pyOpenSSL',
    'ndg-httpsclient',
    'pyasn1'
]

if sys.version_info[0] < 3:
    install_requires += installs_for_two

packages = [
    'quandl',
    'quandl.errors',
    'quandl.model',
    'quandl.operations',
    'quandl.utils'
]

setup(
    name='Quandl',
    description='Package for quandl API access',
    keywords=['quandl', 'API', 'data', 'financial', 'economic'],
    long_description=long_description,
    version=VERSION,
    author='Quandl',
    maintainer='Quandl Development Team',
    maintainer_email='dev@quandl.com',
    url='https://github.com/quandl/quandl-python',
    license='MIT',
    install_requires=install_requires,
    tests_require=[
        'unittest2',
        'flake8',
        'nose',
        'httpretty',
        'mock',
        'factory_boy',
        'jsondate'
    ],
    test_suite="nose.collector",
    packages=packages
)
