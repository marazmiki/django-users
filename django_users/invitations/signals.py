from django.core.signals import Signal

invitation_accepted = Signal(providing_args=['request', 'user', 'invitation'])
invitation_sent = Signal(providing_args=['request', 'invitation', 'user', 'email'])