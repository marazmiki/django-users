from django.core.signals import Signal
from django.contrib.auth.signals import user_logged_in as logged_in

logged_out = Signal(providing_args=['request'])
wrong_password = Signal(providing_args=['request'])
already_logged_in = Signal(providing_args=['request', 'user'])