import os
import sys

if sys.version_info[:2] < (3, 5):
    raise ImportError("""
    This version of quandl-python no longer supports python versions less than 3.5.0. If you're reading this message
    your pip and/or setuptools are outdated. Please run the following to update them:
    
    pip install pip setuptools --upgrade
    
    Then try to reinstall quandl-python
    
    pip install quandl
    """)

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('LONG_DESCRIPTION.rst') as f:
    LONG_DESCRIPTION = f.read()

# Don't import quandl module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'quandl'))
# can only import VERSION successfully after the above line
# ignore flake8 warning that requires imports to be at the top
from version import VERSION  # NOQA

INSTALL_REQUIRES = [
    'pandas >= 0.14',
    'numpy >= 1.8',
    'requests >= 2.7.0',
    'inflection >= 0.3.1',
    'python-dateutil',
    'six',
    'more-itertools'
]

INSTALLS_FOR_TWO = [
    'pyOpenSSL',
    'ndg-httpsclient',
    'pyasn1'
]

if sys.version_info[0] < 3:
    INSTALL_REQUIRES += INSTALLS_FOR_TWO

TEST_REQUIRES = [
        'flake8',
        'nose',
        'httpretty',
        'mock',
        'factory_boy',
        'jsondate',
        'parameterized'
]

PACKAGES = [
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
    long_description=LONG_DESCRIPTION,
    version=VERSION,
    author='Quandl',
    author_email='connect@quandl.com',
    maintainer='Quandl Development Team',
    maintainer_email='connect@quandl.com',
    url='https://github.com/quandl/quandl-python',
    license='MIT',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    install_requires=INSTALL_REQUIRES,
    tests_require=TEST_REQUIRES,
    python_requires='>= 3.5',
    test_suite="nose.collector",
    packages=PACKAGES
)
