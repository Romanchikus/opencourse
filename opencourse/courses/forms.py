from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from . import models


class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = [
            "title",
            "area",
            "descrip",
            "level",
            "extrainfo",
            "language",
            "duration",
            "age",
        ]
        labels = {
            "title": _("Title"),
            "area": _("Area"),
            "descrip": _("Description"),
            "level": _("Level"),
            "extrainfo": _("Extra information"),
            "language": _("Language"),
            "duration": _("Duration"),
            "age": _("Age"),
        }


class CourseSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.field_class = "form-field"

    city = forms.ModelChoiceField(models.City.objects, empty_label=_("City"))
    area = forms.ModelChoiceField(models.CourseArea.objects, empty_label=_("Area"))


class CourseLocationForm(forms.ModelForm):
    class Meta:
        model = models.CourseLocation
        fields = ("location_type", "price", "currency")
        labels = {
            "location_type": _("Location type"),
            "price": _("Price"),
            "currency": _("Currency"),
        }

    currency = forms.ModelChoiceField(models.Currency.objects.all(),)


CourseLocationFormset = inlineformset_factory(
    models.Course, models.CourseLocation, form=CourseLocationForm, extra=1,
)
