from django import forms
from django.utils.translation import ugettext_lazy as _
from . import models


class EnrollmentView(forms.ModelForm):
    class Meta:
        model = models.Enrollment
        fields = [
            "is_active",
        ]
        labels = {
            "is_active": _("Is active"),
        }


class HandoutForm(forms.ModelForm):
    class Meta:
        model = models.Handout
        fields = [
            "name",
            "description",
            "attachment",
            "section",
        ]
        labels = {
            "name": _("Name"),
            "description": _("Description"),
            "attachment": _("Attachment"),
            "section": _("Section"),
        }
