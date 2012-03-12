#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import setuptools
import django_users

def rel(*x):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), *x))

PACKAGE_NAME = 'django-users'

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Framework :: Django'
]

setuptools.setup(
    name             = PACKAGE_NAME,
    version          = django_users.get_version(),
    description      = 'This is a applications set that provides quick and flexible way to manage users in Django projects',
    long_description = open(rel('README.rst')).read(),
    author       = 'marazmiki',
    author_email = 'marazmiki@gmail.com',
    platforms    = ['OS Independent'],
    classifiers  = CLASSIFIERS,
    license      = 'MIT license',
    url          = 'http://pypi.python.org/pypi/django-users',
    download_url = 'https://github.com/marazmiki/django-users/zipball/master',
    install_requires = [
        'Django>=1.3.1',
        'django-guardian',
    ],
    packages = setuptools.find_packages(exclude=['test_project', 'test_project.*']),
    include_package_data = True,
    zip_safe = False
)


