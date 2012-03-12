from django.conf import settings

EMAIL_FORMAT = getattr(settings, 'USERS_INVITE_EMAIL_FORMAT', 'html')
EMAIL_BODY_TPL = getattr(settings, 'USERS_INVITE_EMAIL_BODY_TPL', 'django_users/invitations/email.html')
EMAIL_SUBJECT_TPL = getattr(settings, 'USERS_INVITE_EMAIL_SUBJECT_TPL', 'django_users/invitations/email_subject.txt')
