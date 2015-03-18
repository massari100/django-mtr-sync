from setuptools import setup, find_packages

import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

README = read('README.rst')

setup(
    name='django-mtr-sync',
    packages=find_packages(),
    # package_data={'': ['']},
    version='0.0',
    author='mtr group',
    author_email='inboxmtr@gmail.com',
    url='https://github.com/mtrgroup/django-mtr-sync',
    description="",
    long_description=README,
    classifiers=[
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
    ],
    keywords=['xlsx', 'import data', 'export data'],
    install_requires=['Django >= 1.6'],
)
