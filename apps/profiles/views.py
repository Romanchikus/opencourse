from django.urls import reverse_lazy
from django.views.generic import UpdateView, RedirectView
from django.contrib.auth import get_user_model
from apps.profiles import forms

User = get_user_model()


class ProfessorUpdateView(UpdateView):
    model = User
    template_name = "profiles/professor.html"
    success_url = reverse_lazy('courses:list')
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


class ProfileView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):

        if hasattr(self.request.user, "professor"):
            self.pattern_name = "profiles:professor"
        elif hasattr(self.request.user, "student"):
            self.pattern_name = "profiles:student"

        return super().get_redirect_url(*args, **kwargs)
