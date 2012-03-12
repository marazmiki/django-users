from django import test
from django.conf.urls.defaults import url, patterns
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django_users.authentication.forms import AuthenticationForm
from django_users.authentication.views import Login, Logout
from django_users.authentication.signals import already_logged_in, wrong_password, logged_in
from django_users import settings as settings
from django_users.tests import create_user, TriggerException, USERNAME, PASSWORD, EMAIL, UserTestBase

###############################################################################
# SOME HELPERS CLASSES                                                        #
###############################################################################


class TestAuthenticationForm(AuthenticationForm):
    pass

###############################################################################
# SOME PREDEFINED CONSTANTS                                                   #
###############################################################################

LOGIN_CUSTOM_TEMPLATE_NAME = 'django_users/tests/authentication/login.html'
LOGIN_CUSTOM_LOGIN_URL     = '/django_login/'
LOGIN_CUSTOM_REDIRECT_URL  = '/django_index/'
LOGIN_CUSTOM_FORM_CLASS    = TestAuthenticationForm

###############################################################################
# TEST SUITES                                                                 #
###############################################################################

class LoginTest(UserTestBase):
    urls = 'django_users.authentication.tests'

    def setUp(self):
        super(LoginTest, self).setUp()
        self.url  = reverse('django_users_login')

    def test_get_when_user_is_anonymous(self):
        resp = self.client.get(self.url)
        self.assertEquals(200, resp.status_code)
        self.assertIn(u'django-users login', resp.content)

    def test_get_when_user_is_authenticated(self):
        self.authenticate_user()
        resp = self.client.get(self.url, follow=False)
        self.assertEquals(302, resp.status_code)

    def test_post_when_user_is_authenticated(self):
        self.authenticate_user()
        resp = self.client.post(self.url, {'username': USERNAME, 'password': PASSWORD})
        self.assertEquals(302, resp.status_code)

    def test_authentication(self):
        assert self.client.login(username=USERNAME, password=PASSWORD)

    def test_wrong_authentication(self):
        resp = self.client.post(self.url, {
            'username': USERNAME,
            'password': PASSWORD+'NOT'})

        self.assertTrue(200 == resp.status_code)
        self.assertTrue('form' in resp.context)
        self.assertTrue(hasattr(resp.context['form'], 'errors'))
        self.assertTrue('__all__' in resp.context['form'].errors)

    # Test
    def test_custom_login_url(self):
        self.assertNotEquals(settings.LOGIN_URL, LOGIN_CUSTOM_LOGIN_URL)

    def test_custom_redirect_url(self):
        ''  # redirect_url = settings.LOGIN_REDIRECT_URL
        self.assertNotEquals(settings.LOGIN_REDIRECT_URL, LOGIN_CUSTOM_REDIRECT_URL)

    def test_custom_form_class(self):
        ''  # form_class = settings.LOGIN_FORM
        self.assertNotEquals(settings.LOGIN_FORM, LOGIN_CUSTOM_FORM_CLASS)

    def test_custom_template_name(self):
        ''  # template_name = settings.LOGIN_TEMPLATE_NAME

    ##
    # signals
    def test_signal_already_logged_in(self):
        def check_call():
            already_logged_in.connect(receiver=self.trigger)
            self.authenticate_user()
            self.client.post(self.url, {'username': USERNAME,
                                        'password': PASSWORD})
        self.assertRaises(TriggerException, check_call)
        already_logged_in.disconnect(receiver=self.trigger)

    def test_signal_wrong_password(self):
        def check_call():
            wrong_password.connect(receiver=self.trigger)
            self.client.post(self.url, {'username': USERNAME,
                                        'password': PASSWORD + '_WRONG'})
        self.assertRaises(TriggerException, check_call)
        wrong_password.disconnect(receiver=self.trigger)


    def test_signal_logged_in(self):
        def check_call():
            logged_in.connect(receiver=self.trigger)
            self.authenticate_user()
        self.assertRaises(TriggerException, check_call)
        logged_in.disconnect(receiver=self.trigger)

###############################################################################

def index(request):
    return render(request, 'django_users/tests/index.html')


urlpatterns = patterns('',
    url('^index/$', index),
    url('^django_logout/$',  Logout.as_view(), name='django_users_logout'),
    url('^django_login/$',   Login.as_view(template_name = LOGIN_CUSTOM_TEMPLATE_NAME,
                                           login_url     = LOGIN_CUSTOM_LOGIN_URL,
                                           redirect_url  = LOGIN_CUSTOM_REDIRECT_URL,
                                           form_class    = LOGIN_CUSTOM_FORM_CLASS,
                                          ), name='django_users_login'),

)