from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django_users.invitations import settings
import datetime
import uuid

class Invitation(models.Model):
    inviting = models.ForeignKey(User,
        related_name = 'inviting',
        verbose_name = _('inviting'))
    invited = models.ForeignKey(User,
        related_name = 'invited',
        verbose_name = _('invited'),
        blank = True,
        null = True)
    email = models.EmailField(_('e-mail'),
        blank = True,
        null = True)
    message = models.TextField(_('message'),
        blank = True,
        default = '')

    # readonly codes
    code = models.CharField(_('invitation code'),
        editable = False,
        max_length = 255,
        default = '')
    date_created = models.DateTimeField(_('created'),
        default = datetime.datetime.now,
        editable = False)
    date_accepted = models.DateTimeField(_('accepted'),
        default  = None,
        null     = True,
        editable = False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.generate_code()
        return super(Invitation, self).save(*args, **kwargs)

    def __unicode__(self):
        return ''

    def generate_code(self):
        while True:
            self.code = uuid.uuid4().hex
            if self.__class__.objects.filter(code=self.code).count() == 0:
                break

    def get_email_subject(self, request=None):
        return render_to_string(settings.EMAIL_SUBJECT_TPL, {
            'request': request,
            'invite': self,
        })

    def get_email_body(self, request=None):
        return render_to_string(settings.EMAIL_BODY_TPL, {
            'request': request,
            'invite': self,
        })

    def get_absolute_url(self):
        return ''

    @models.permalink
    def get_revoke_url(self):
        return 'django_users_invites_revoke', [self.code]
    class Meta:
        db_table = 'django_users_invitation'
        verbose_name = _('invite')
        verbose_name_plural = _('invitations')
