from django.urls import reverse_lazy
from django.views.generic import CreateView
from opencourse.users.forms import UserCreationForm
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView,
)


class SignUpView(CreateView):
    template_name = "users/signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("users:signup")


class LoginView(BaseLoginView):
    template_name = "users/login.html"

    def get_success_url(self):
        redirect_url = self.get_redirect_url()
        return redirect_url or reverse_lazy("users:signup")


class LogoutView(BaseLogoutView):
    def get_next_page(self):
        return reverse_lazy("users:signup")
