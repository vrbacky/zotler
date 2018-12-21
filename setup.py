#!/usr/bin/env python3

import codecs
from collections import namedtuple
import os
import re
import sys

header = namedtuple('HEADER', ['name', 'version', 'author', 'license'])


def get_header_parameter(parameter, match):
    try:
        return match.group(1)
    except AttributeError:
        raise AttributeError(f'Unable to find {parameter} string.')


def get_header_info(*file_paths):
    header_file = read(*file_paths)

    name_match = re.search(r'^__name__ = [\'"]([^\'"]*)[\'"]',
                           header_file, re.M)
    version_match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]',
                              header_file, re.M)
    author_match = re.search(r'^__author__ = [\'"]([^\'"]*)[\'"]',
                             header_file, re.M)
    license_match = re.search(r'^__license__ = [\'"]([^\'"]*)[\'"]',
                              header_file, re.M)

    header_data = header(name=get_header_parameter('name', name_match),
                         version=get_header_parameter('version', version_match),
                         author=get_header_parameter('author', author_match),
                         license=get_header_parameter('license', license_match),
                         )
    return header_data


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return tuple(line for line in lineiter if line and not line.startswith("#"))


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, *parts), "r").read()


def get_long_description():
    try:
        with open('readme.md', 'r') as readme_file:
            return readme_file.read()
    except IOError:
        print('Cannot find readme.md file. Long description will be empty.\n')
        return ''


def get_requirements():
    requirements_file = 'requirements.txt'
    requirements = parse_requirements(requirements_file)
    return tuple(str(r) for r in requirements)


parsed_header = get_header_info('zotler', '__init__.py')

try:
    from setuptools import setup, find_packages
except ImportError:
    raise RuntimeError("Python package setuptools hasn't been installed.\n"
                       "Please install setuptools before installing "
                       "{}.\n".format(parsed_header.name))
if sys.version_info < (3, 6, 0):
    raise RuntimeError('Python 3.6.0 or higher required.\n')

setup(name=parsed_header.name,
      version=parsed_header.version,
      description='A script searching for and removing orphan'
                  'attachments left by ZotFile.',
      long_description=get_long_description(),
      install_requires=get_requirements(),
      keywords='Zotero ZotFile attachment cleanup',
      url='https://github.com/vrbacky/zotler',
      author=parsed_header.author,
      author_email='vrbacky@fnhk.cz',
      maintainer=parsed_header.author,
      maintainer_email='vrbacky@fnhk.cz',
      license=parsed_header.license,
      zip_safe=False,
      packages=find_packages(exclude=['docs', 'test']),
      test_suite='test',
      include_package_data=True,
      data_files=[],
      entry_points={
          'console_scripts': [
              'zotler = bin.zotler:main',
          ],
          'gui_scripts': [
              'zotler_gui = bin.zotler_gui:main'
          ],
      },
      classifiers=('Development Status :: 3 - Alpha',
                   'Environment :: Console',
                   'Intended Audience :: End Users/Desktop',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 3.6',
                   'Topic :: Utilities',
                   )
      )
