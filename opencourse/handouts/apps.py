from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class HandoutsConfig(AppConfig):
    name = "opencourse.handouts"
    verbose_name = _("Handouts")
