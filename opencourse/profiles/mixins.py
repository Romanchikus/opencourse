from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy


class ProfessorRequiredMixin(PermissionRequiredMixin):
    permission_required = "profiles.access_professor_pages"
    login_url = reverse_lazy("profiles:403")


class StudentRequiredMixin(PermissionRequiredMixin):
    permission_required = "profiles.access_student_pages"
    login_url = reverse_lazy("profiles:403")
