import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('LONG_DESCRIPTION.rst') as f:
    long_description = f.read()

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

ndg_httpsclient_version = 'ndg-httpsclient'
if sys.version_info[0] < 3:
    ndg_httpsclient_version = 'ndg-httpsclient == 0.3.0'
    install_requires += installs_for_two

packages = [
    'quandl',
    'quandl.errors',
    'quandl.model',
    'quandl.operations'
]

setup(
    name='quandl',
    description='Package for quandl API access',
    long_description=long_description,
    version='3.0.0',
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
        ndg_httpsclient_version
    ],
    test_suite="nose.collector",
    packages=packages
)
