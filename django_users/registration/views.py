from django.contrib.auth import authenticate
from django.shortcuts import  redirect
from django.views.generic.edit import FormView
from django_users import settings
from django_users.registration.forms import RegistrationForm
from django_users.views import RequestFormMixin

class Registration(RequestFormMixin, FormView):
    template_name = 'django_users/registration/registration.html'
    form_class = RegistrationForm

    def dispatch(self,request, *args, **kwargs):
        #if request.user.is_authenticated():
        #    return redirect(settings.LOGIN_REDIRECT_URL)
        return super(Registration, self).dispatch(request, *args, **kwargs)

    def on_success(self, request, user):
        if settings.REGISTRATION_AUTO_AUTHENTICATE:
            auth = authenticate(username = user.username,
                                password = request.POST.get('password'))

            if auth is not None:
                return redirect(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        return self.on_success(self.request, user)