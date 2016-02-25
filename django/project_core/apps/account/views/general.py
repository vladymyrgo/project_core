from django.views.generic import FormView, CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse_lazy

from account.forms import SignUpForm
from account.models import User


class SignUpView(CreateView):
    model = User
    template_name = 'page/sign_up.jinja2'
    form_class = SignUpForm
    success_url = '/'


class LoginView(FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('page:cabinet')
    template_name = 'page/login.jinja2'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(email=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)
