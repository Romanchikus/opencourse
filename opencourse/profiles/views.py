from django.urls import reverse_lazy
from django.views.generic import UpdateView, RedirectView
from django.contrib.auth import get_user_model
from opencourse.profiles import forms

User = get_user_model()


class ProfileUpdateView(UpdateView):
    model = User
    fields = ["first_name", "last_name"]
    formset_class = None

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = self.formset_class(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = self.formset_class(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['formset']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)


class ProfessorUpdateView(ProfileUpdateView):
    template_name = "profiles/profile.html"
    success_url = reverse_lazy('courses:list')
    formset_class = forms.ProfessorFormSet


class StudentUpdateView(ProfileUpdateView):
    template_name = "profiles/profile.html"
    success_url = reverse_lazy('courses:search')
    formset_class = forms.StudentFormSet


class ProfileView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if hasattr(self.request.user, "professor"):
            return reverse_lazy("profiles:professor")
        elif hasattr(self.request.user, "student"):
            return reverse_lazy("profiles:student")
        return super().get_redirect_url(*args, **kwargs)


class DispatchLoginView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if hasattr(self.request.user, "professor"):
            if self.request.user.professor.course_set.exists():
                return reverse_lazy("courses:list")
            else:
                return reverse_lazy("courses:create")
        return reverse_lazy("courses:search")
