from django.conf.urls.defaults import *
from django_users.invitations.urls import invites_urlpatterns
from django_users.authentication.views import Login, Logout
from django_users.registration.views import Registration

# Authentication views
login_urlpatterns = patterns('',
    url('^login/$',         Login.as_view(),        name='django_users_login'),
    url('^logout/$',        Logout.as_view(),       name='django_users_logout'),
)

# Registration urlpatterns
registration_urlpatterns = patterns('',
    url('^registration/$',  Registration.as_view(), name='django_users_registration'),
)

urlpatterns = login_urlpatterns + registration_urlpatterns
urlpatterns = invites_urlpatterns + urlpatterns
