from Quandl import __version__, __authors__, __maintainer__, __email__, __url__, __license__
from Quandl import __name__ as package_name
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from pip.req import parse_requirements
    requirements = list(parse_requirements('requirements.txt'))
except:
    requirements = []
install_requires=[str(req).split(' ')[0].strip() for req in requirements if req.req and not req.url]
print('Install requirements found in requirements.txt: %r' % install_requires)
dependency_links=[req.url for req in requirements if req.url]
print('Dependencies found in requirements.txt: %r' % dependency_links)


setup(
      name = package_name,
      description = 'Package for Quandl API access',
      long_description = open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
      version = __version__,
      author = ", ".join(__authors__),
      maintainer = __maintainer__,
      maintainer_email = __email__,
      url = __url__,
      license = __license__,
      install_requires = [
        "pandas >= 0.14",
        "numpy >= 1.8",
      ],
      # install_requires = install_requires,
      dependency_links = dependency_links,
      packages = ['Quandl'],
)
