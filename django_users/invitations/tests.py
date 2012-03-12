# -*- coding: utf-8 -*-

from django import test
from django.core import mail
from django.core.urlresolvers import reverse
from django_users.tests import UserTestBase, PASSWORD
from django_users.invitations.models import Invitation

class InvitationTest(UserTestBase):
    urls = 'django_users.invitations.urls'
    view_name = 'django_users_invites_list'
    invite_email = 'somewhere@microsoft.com'

    @property
    def url(self):
        return reverse(self.view_name)

    def setUp(self):
        super(InvitationTest, self).setUp()
        self.authenticate_user()

    def test_403_if_anonymous_user(self):
        self.unauthenticate()
        page = self.client.get(self.url)
        self.assertEquals(302, page.status_code)


class ListInviteTest(InvitationTest):
    view_name = 'django_users_invites_list'

    def test_list_empty(self):
        page = self.client.get(self.url)
        self.assertEquals(200, page.status_code)
        self.assertIn('available_invites', page.context)
        self.assertIn('invited_by_me', page.context)
        self.assertEquals(0, page.context['available_invites'].count())
        self.assertEquals(0, page.context['invited_by_me'].count())

    def test_has_1_available_invitation(self):
        invitation = Invitation.objects.create(inviting=self.user)
        page = self.client.get(self.url)

        self.assertEquals(200, page.status_code)
        self.assertIn('available_invites', page.context)
        self.assertIn('invited_by_me', page.context)
        self.assertEquals(1, page.context['available_invites'].count())
        self.assertEquals(0, page.context['invited_by_me'].count())


    def test_has_1_pending_invitation(self):
        invitation = Invitation.objects.create(inviting=self.user, email=self.invite_email)

        page  = self.client.get(self.url)

        self.assertEquals(200, page.status_code)
        self.assertIn('available_invites', page.context)
        self.assertIn('invited_by_me', page.context)
        self.assertEquals(0, page.context['available_invites'].count())
        self.assertEquals(1, page.context['invited_by_me'].count())
        self.assertIn(self.invite_email, page.content)
        self.assertIn(invitation.get_revoke_url(), page.content)

    def test_has_1_user_invited(self):
        invitation = Invitation.objects.create(inviting  = self.user,
            invited = self.another_user,
            email   = self.another_user.email)

        page  = self.client.get(self.url)

        self.assertEquals(200, page.status_code)
        self.assertIn('available_invites', page.context)
        self.assertIn('invited_by_me', page.context)
        self.assertEquals(0, page.context['available_invites'].count())
        self.assertEquals(1, page.context['invited_by_me'].count())
        self.assertIn(self.another_user.username,     page.content)
        self.assertNotIn(invitation.get_revoke_url(), page.content)


class SendInviteTest(InvitationTest):
    view_name = 'django_users_invites_send'

    def send_invite(self):
        return self.client.post(self.url, {
            'email'    : self.invite_email,
            'password' : PASSWORD,
            'message'  : 'Testing the django-users invitations'
        })

    def test_404_if_no_invitations(self):
        page = self.send_invite()
        self.assertEquals(404, page.status_code)

    def test_404_if_no_unused_invitations(self):
        for i in xrange(5):
            Invitation.objects.create(inviting=self.user, email=self.invite_email)
        page = self.send_invite()
        self.assertEquals(404, page.status_code)


    def test_scenario(self):
        Invitation.objects.create(inviting=self.user)

        page = self.send_invite()

        self.assertEquals(1, Invitation.objects.filter(inviting=self.user).count())
        self.assertEquals(0, Invitation.objects.filter(email__isnull=True).count())

        self.assertEquals(1, len(mail.outbox))
        email = mail.outbox[0]

        invitation = Invitation.objects.get()

        self.assertEquals(self.user, invitation.inviting)
        self.assertEquals(self.invite_email, invitation.email)

        self.assertIn(invitation.get_absolute_url(), email.body)

class RevokeInviteTest(InvitationTest):
    view_name = 'django_users_invites_revoke'

    def setUp(self):
        super(RevokeInviteTest,self).setUp()
        self.invite = Invitation.objects.create(inviting=self.user)

    @property
    def url(self):
        return self.invite.get_revoke_url()

    def test_404_if_tries_revoke_empty_invitation(self):
        page = self.client.get(self.url)
        self.assertEquals(404, page.status_code)

    def test_1(self):
        self.invite.email = self.invite_email
        self.invite.save()

        page = self.client.get(self.url)
        self.assertEquals(200, page.status_code)
        self.assertIn('form', page.content)

        page = self.client.post(self.url)
        self.assertEquals(302, page.status_code)

        page = self.client.get(self.url)
        self.assertEquals(404, page.status_code)

        self.assertEquals(1, Invitation.objects.filter(inviting=self.user).count())
        self.assertEquals(1, Invitation.objects.filter(email__isnull=True).count())

        invitation = Invitation.objects.get()
