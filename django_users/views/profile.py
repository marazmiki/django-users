from django.views.generic.edit import FormView
from django_users.views import ProfileBase

class EditProfile(ProfileBase, FormView):
    ''

class Avatar(ProfileBase):
    ''