import os
import sys

if sys.version_info[:2] < (3, 5):
    raise ImportError("""
    This version of Nasdaq Data Link no longer supports python versions less than 3.5.0. If you're
    reading this message your pip and/or setuptools are outdated. Please run the following to
    update them:

    pip install pip setuptools --upgrade

    Then try to reinstall nasdaq-data-link:

    pip install nasdaq-data-link
    """)

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('LONG_DESCRIPTION.rst') as f:
    LONG_DESCRIPTION = f.read()

# Don't import nasdaqdatalink module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'nasdaqdatalink'))
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
    'nasdaqdatalink',
    'nasdaqdatalink.errors',
    'nasdaqdatalink.model',
    'nasdaqdatalink.operations',
    'nasdaqdatalink.utils'
]

setup(
    name='Nasdaq Data Link',
    description='Package for Nasdaq Data Link API access',
    keywords=['nasdaq data link', 'nasdaq', 'datalink', 'API', 'data', 'financial', 'economic'],
    long_description=LONG_DESCRIPTION,
    version=VERSION,
    author='Nasdaq Data Link',
    author_email='connect@data.nasdaq.com',
    maintainer='Nasdaq Data Link Development Team',
    maintainer_email='connect@data.nasdaq.com',
    url='https://github.com/Nasdaq/data-link-python',
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
