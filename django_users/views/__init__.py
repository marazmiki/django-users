from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django_users import settings

class LoginRequiredMixin(object):
    """
    """
    def dispatch(self, request, *args, **kwargs):
        if self.check_logged_in(request.user):
            return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
        return self.not_logged_in(self)

    def check_logged_in(self, user):
        """
        """
        return user.is_authenticated()

    def not_logged_in(self):
        """
        """
        return redirect(settings.LOGIN_URL)


class RequestFormMixin(object):
    """
    """
    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instanciating the form.
        """
        kwargs = super(RequestFormMixin, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class ProfileBase(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileBase, self).dispatch(request, *args, **kwargs)


class DecoratorChainingMixin(object):
    def dispatch(self, *args, **kwargs):
        decorators = getattr(self, 'decorators', [])
        base = super(DecoratorChainingMixin, self).dispatch

        for decorator in decorators:
            base = decorator(base)
        return base(*args, **kwargs)