from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_users import settings

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label=_('username'),
        max_length = 30)
    password = forms.CharField(label=_('password'),
        help_text = _('please use complicated password'),
        widget    = forms.PasswordInput())
    confirm = forms.CharField(label=_('confirm password'),
        help_text = _('please retype your password to avoid mistakes'),
        widget=forms.PasswordInput())
    email = forms.EmailField(label=_('e-mail'))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(RegistrationForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        if username in settings.DISALLOWED_USERNAMES:
            raise forms.ValidationError, _('this username is restricted for usage. Please choose another')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError, _('this e-mail address is already used')
        return email

    def clean_confirm(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm']:
            raise forms.ValidationError, _('passwords doesn\'t match')
        return self.cleaned_data['confirm']

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm', 'email']