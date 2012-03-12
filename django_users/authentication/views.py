from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django_users.authentication.signals import logged_in, logged_out, wrong_password, already_logged_in
from django_users import settings

class Login(View):
    """
    Views for user authentication
    """
    login_url     = settings.LOGIN_URL
    redirect_url  = settings.LOGIN_REDIRECT_URL
    form_class    = settings.LOGIN_FORM
    template_name = settings.LOGIN_TEMPLATE_NAME

    def __init__(self, *args, **kwargs):
        if isinstance(self.form_class, basestring):
            self.form_class = settings.extract_class(self.form_class)
        super(Login, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """
        """
        if request.user.is_authenticated():
            already_logged_in.send(sender = None,
                request = request,
                user    = request.user)
            return self.on_already_logged_in(request)
        return super(Login, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """
        """
        return render(request, self.template_name, {
            'form': self.form_class(request=request),
        })

    def post(self, request):
        """
        """
        form = self.form_class(request = request,
                               data    = request.POST,
                               files   = request.FILES)
        if form.is_valid():
            login(request, form.get_user())
            return self.on_success(request, form)

        wrong_password.send(sender=None,
            request = request)

        return render(request, self.template_name, {
            'form': form,
        })

    def on_success(self, request, form):
        return redirect(self.redirect_url)

    def on_already_logged_in(self, request):
        return redirect(self.redirect_url)


class Logout(View):
    logout_url = settings.LOGOUT_URL
    template_name = settings.LOGOUT_TEMPLATE_NAME

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(Logout, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        return self.get(request)