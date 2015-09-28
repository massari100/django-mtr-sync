from setuptools import setup, find_packages

import os

from mtr.sync import VERSION


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

README = read('README.md')

version_tuple = VERSION
version = ".".join(str(v) for v in version_tuple)

setup(
    name='django-mtr-sync',
    packages=find_packages(),
    # package_data={'': ['']},
    version=version,
    author='mtr group',
    author_email='inboxmtr@gmail.com',
    url='https://github.com/mtrgroup/django-mtr-sync',
    description="",
    long_description=README,
    classifiers=[
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    keywords=['xlsx', 'import data', 'export data'],
    install_requires=['Django >= 1.6'],
)
