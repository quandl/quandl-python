from setuptools import find_packages, setup


DESCRIPTION = 	"""\
Basic wrapper to return datasets from the Quandl website as Pandas dataframe objects with a timeseries index, or as a numpy array.
"""

setup(
    name='quandl',
    description=DESCRIPTION,
    author="Enthought, Inc.",
    packages=find_packages(),
)
