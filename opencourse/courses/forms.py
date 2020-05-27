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
            "city",
        ]
        labels = {
            "title": _("Title"),
            "area": _("Area"),
            "descrip": _("Description"),
            "level": _("Level"),
            "extrainfo": _("Extra information"),
            "language": _("Language"),
            "duration": _("Duration"),
            "city": _("City"),
        }


class CourseSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.field_class = "form-field"

    city = forms.ModelChoiceField(models.City.objects, empty_label=_("City"), required=False)
    area = forms.ModelChoiceField(models.CourseArea.objects, empty_label=_("Area"), required=True)


class CourseLocationForm(forms.ModelForm):
    currency = forms.ModelChoiceField(models.Currency.objects.all(), label=_("Currency"))

    class Meta:
        model = models.CourseLocation
        fields = ("location_type", "price", "currency")
        labels = {
            "location_type": _("Location type"),
            "price": _("Price"),
        }


CourseLocationFormset = inlineformset_factory(
    models.Course, models.CourseLocation, form=CourseLocationForm, extra=1,
)


class EnrollmentView(forms.ModelForm):
    class Meta:
        model = models.Enrollment
        fields = [
            "accepted",
        ]
        labels = {
            "accepted": _("accepted"),
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
