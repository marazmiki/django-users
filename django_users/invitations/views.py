from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django_users.invitations.forms import InvitationForm
from django_users.invitations import settings
from django_users.invitations.models import Invitation
from django.core.mail import EmailMessage
from django_users.views import ProfileBase, RequestFormMixin


class Send(ProfileBase, RequestFormMixin, UpdateView):
    form_class = InvitationForm
    model = Invitation
    template_name = 'django_users/invitations/send.html'

    def get_queryset(self):
        return self.model.objects.filter(inviting      = self.request.user,
                                         invited       = None,
                                         email__isnull = True,
                                         date_accepted = None)

    def get_object(self, queryset=None):
        slice = self.get_queryset()[:1]
        if slice:
            return slice[0]
        raise Http404, 'There are no invitations'

    def get_success_url(self):
        return 'django_users_invites_list'

    def get_context_data(self, **kwargs):
        kwargs = super(Send, self).get_context_data(**kwargs)
        kwargs.update({
            'available_invites': self.get_queryset()
        })
        return kwargs

    def form_valid(self, form):
        invite = form.save(commit=False)
        invite.inviting = self.request.user
        invite.save()

        email = EmailMessage(subject = invite.get_email_subject(self.request),
                             body    = invite.get_email_body(self.request),
                             to      = [invite.email])
        email.content_subtype = settings.EMAIL_FORMAT
        email.send()

        return redirect(self.get_success_url())

class List(ProfileBase, ListView):
    template_name = 'django_users/invitations/list.html'
    context_object_name = 'invitations'
    model = Invitation

    def get_queryset(self):
        return super(ListView, self).get_queryset().filter(
            inviting = self.request.user
        )

    def get_context_data(self, **kwargs):
        return {
            'invited_by_me': self.get_queryset().exclude(email=None),
            'available_invites': self.get_queryset().filter(email__isnull=True),
            'form': InvitationForm(request=self.request),
        }

class Revoke(ProfileBase, DetailView):
    template_name = 'django_users/invitations/revoke.html'
    context_object_name = 'invitation'
    queryset = Invitation.objects.filter(email__isnull=False, invited=None)

    def get_object(self, queryset=None):
        queryset = self.get_queryset().filter(inviting=self.request.user)
        return get_object_or_404(queryset, code=self.kwargs['code'])

    def get_success_url(self):
        return 'django_users_invites_list'

    def post(self, request, **kwargs):
        invitation = self.get_object()
        invitation.email = None
        invitation.generate_code()
        invitation.save()

        return redirect(self.get_success_url())