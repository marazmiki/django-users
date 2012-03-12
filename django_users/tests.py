# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django import test

###############################################################################

USERNAME = 'bender'
PASSWORD = '2716057'
EMAIL    = 'bender@ilovebender.com'

ANOTHER_USERNAME = 'flexo'
ANOTHER_PASSWORD = '3370318'
ANOTHER_EMAIL    = 'flexo@iloveflexo.com'

class TriggerException(Exception):
    pass

def create_user():
    return User.objects.create_user(username = USERNAME,
                                    password = PASSWORD,
                                    email    = EMAIL)

def create_another_user():
    return User.objects.create_user(username = ANOTHER_USERNAME,
                                    password = ANOTHER_PASSWORD,
                                    email    = ANOTHER_EMAIL)


class UserTestBase(test.TestCase):
    def setUp(self):
        self.client = test.Client()
        self.user = create_user()
        self.another_user = create_another_user()

    def authenticate_user(self):
        self.client.login(username=USERNAME, password=PASSWORD)

    def authenticate_another_user(self):
        self.client.login(username=ANOTHER_USERNAME, password=ANOTHER_PASSWORD)

    def unauthenticate(self):
        self.client.logout()

    def trigger(self, *args, **kwargs):
        raise TriggerException
