from django.urls import reverse_lazy
from django.views.generic import FormView
from opencourse.users.forms import UserCreationForm


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("users:signup")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
