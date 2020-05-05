from braces.views import GroupRequiredMixin
from django.urls import reverse_lazy


class ProfessorRequiredMixin(GroupRequiredMixin):
    group_required = "professors"
    login_url = reverse_lazy("profiles:forbidden")


class StudentRequiredMixin(GroupRequiredMixin):
    group_required = "students"
    login_url = reverse_lazy("profiles:forbidden")
