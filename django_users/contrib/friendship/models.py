# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import datetime

class Friendship(models.Model):
    user = models.ForeignKey(User,
        related_name = 'friendship_users',
        verbose_name = _('user'))
    friend = models.ForeignKey(User,
        related_name = 'friends',
        verbose_name = _('friend'))
    date_created = models.DateTimeField(_('created'),
        editable = False,
        default  = datetime.datetime.now)

    def __unicode__(self):
        return unicode(self.friend)

    class Meta:
        verbose_name = _('friend relation')
        verbose_name_plural = _('friend relations')