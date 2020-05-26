from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EnrollmentsConfig(AppConfig):
    name = "opencourse.handouts"
    verbose_name = _("Enrollments")
