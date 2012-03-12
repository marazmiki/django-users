from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_users.invitations.models import Invitation
from django_users.invitations.signals import invitation_accepted
from django_users.registration.forms import RegistrationForm
import datetime


class InvitationForm(forms.ModelForm):
    password = forms.CharField(label=_('password'),
        required = True,
        widget   = forms.PasswordInput())

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(InvitationForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError, _('Enter the e-mail address')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        username = self.request.user.username

        if authenticate(username=username, password=password) is None:
            raise forms.ValidationError, _('Wrong password')

        return password

    class Meta:
        model = Invitation
        fields = ['email', 'message', 'password']


class InvitationRegistrationForm(RegistrationForm):
    invite = forms.CharField(label=_('invitation code'))

    def clean_invite(self):
        try:
            return Invitation.objects.get(code=self.cleaned_data['invite'])
        except Invitation.DoesNotExist, e:
            raise forms.ValidationError, _('Wrong invitation code')

    def save(self, *args, **kwargs):
        parent = super(InvitationRegistrationForm, self).save(*args, **kwargs)

        # Update the invitation
        invite = self.cleaned_data['invite']
        invite.invited = User.objects.get(username=self.cleaned_data['username'])
        invite.date_accepted = datetime.datetime.now()
        invite.save()

        # Send the
        invitation_accepted.send(request = self.request,
                                 invitation = invite,
                                 user       = invite.invited)
        return parent