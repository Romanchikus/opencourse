from django.urls import reverse_lazy
from django.views.generic import CreateView
from opencourse.users.forms import UserCreationForm


class SignUpView(CreateView):
    template_name = "users/signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("users:signup")
