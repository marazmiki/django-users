from django.conf.urls.defaults import *
from django_users.invitations.views import Send, List, Revoke

invites_urlpatterns = patterns('',
    url('^$',        List.as_view(),   name='django_users_invites_list'),
    url('^send/$',   Send.as_view(),   name='django_users_invites_send'),
    url('^revoke/(?P<code>\w+)/$', Revoke.as_view(), name='django_users_invites_revoke'),
)

urlpatterns = patterns('', ) + invites_urlpatterns