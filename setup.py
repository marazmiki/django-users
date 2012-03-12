#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import django_users

setuptools.setup(
    package  = 'django-users',
    version  = django_users.get_version(),
    packages = setuptools.find_packages(),
)