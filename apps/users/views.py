from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView,
)
from apps.users import forms

User = get_user_model()


class SignUpView(CreateView):
    template_name = "users/signup.html"
    form_class = forms.UserCreationForm
    success_url = reverse_lazy("users:login")


class LoginView(BaseLoginView):
    template_name = "users/login.html"

    def get_success_url(self):
        redirect_url = self.get_redirect_url()
        return redirect_url or reverse_lazy("courses:create")


class LogoutView(BaseLogoutView):
    def get_next_page(self):
        return reverse_lazy("users:login")


class ProfessorUpdateView(UpdateView):
    model = User
    template_name = "users/update_professor.html"
    success_url = reverse_lazy('users:professor_update')
    fields = ["first_name", "last_name"]

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(ProfessorUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['professor_formset'] = forms.ProfessorFormSet(self.request.POST, instance=self.object)
            context['professor_formset'].full_clean()
        else:
            context['professor_formset'] = forms.ProfessorFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['professor_formset']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)

