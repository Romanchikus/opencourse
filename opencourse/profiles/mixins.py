from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse


class ProfessorRequiredMixin(PermissionRequiredMixin):
    permission_required = "profiles.access_professor_pages"
    login_url = reverse_lazy("profiles:403")


class StudentRequiredMixin(PermissionRequiredMixin):
    permission_required = "profiles.access_student_pages"
    login_url = reverse_lazy("profiles:403")


class JsonFormMixin:
    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse(form.data)

    def form_invalid(self, form):
        data = {
            "success": False,
            "errors": {k: v[0] for k, v in form.errors.items()},
        }
        return JsonResponse(data, status=400)
