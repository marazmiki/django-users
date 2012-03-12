from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
import datetime
import uuid

class Activation(models.Model):
    ''
