from django.conf import settings
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured

def extract_class(target):
    try:
        module_name, att_name = target.rsplit('.', 1)
        module = import_module(module_name)
        attribute = getattr(module, att_name)

    except ValueError:
        raise ImproperlyConfigured, "Wrong format for class"

    except ImportError:
        raise ImproperlyConfigured, "The {module} module not found".format(module=module_name)

    except AttributeError:
        raise ImproperlyConfigured, "The {mod} module has no {att} attribute".format(
            mod = module,
            att = att_name)
    else:
        return attribute



# Login settings
LOGIN_URL = getattr(settings, 'USERS_LOGIN_URL', settings.LOGIN_URL)
LOGIN_REDIRECT_URL = getattr(settings, 'USERS_LOGIN_REDIRECT_URL', settings.LOGIN_REDIRECT_URL)
LOGIN_FORM = getattr(settings, 'USERS_LOGIN_FORM', 'django_users.authentication.forms.AuthenticationForm')
LOGIN_TEMPLATE_NAME = getattr(settings, 'USERS_LOGIN_TEMPLATE_NAME', 'django_users/authentication/login.html')

# Logout settings
LOGOUT_URL = getattr(settings, 'USERS_LOGOUT_URL', settings.LOGOUT_URL)
LOGOUT_TEMPLATE_NAME = getattr(settings, 'USERS_LOGOUT_TEMPLATE_NAME', 'django_users/authentication/logout.html')

# Registration settings
REGISTRATION_ENABLED = getattr(settings, 'USERS_REGISTRATION_ENABLED', True)
REGISTRATION_ACTIVATE_USERS = getattr(settings, 'USERS_REGISTRATION_ACTIVATE_USERS', True)
REGISTRATION_AUTO_AUTHENTICATE = getattr(settings, 'USERS_REGISTRATION_AUTO_AUTHENTICATE', True)

DISALLOWED_USERNAMES = getattr(settings, 'USERS_DISALLOWED_USERNAMES', ['admin', 'www', 'ftp', 'root'])