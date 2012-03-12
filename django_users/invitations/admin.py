from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django_users.invitations.models import Invitation

class InvitationAdmin(admin.ModelAdmin):
    list_display = ['code', 'inviting', 'invited', 'email', 'date_created', 'date_accepted', 'state']
    raw_id_fields = ['inviting', 'invited']

    def state(self, invitation):
        if not invitation.email:
            return _('New')
        if not invitation.invited:
            return _('Pending')
        return _('Used')

admin.site.register(Invitation, InvitationAdmin)