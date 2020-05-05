from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from opencourse.courses import models


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
        labels = {"descrip": _("Description"), "extrainfo": _("Extra information")}


class CourseSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.field_class = "form-field"

    city = forms.ModelChoiceField(models.City.objects, empty_label="City")
    area = forms.ModelChoiceField(models.CourseArea.objects, empty_label="Area")


class CourseLocationForm(forms.ModelForm):
    class Meta:
        model = models.CourseLocation
        fields = ("location_type", "price", "currency")

    currency = forms.ModelChoiceField(
        models.Currency.objects.all(),
        initial=models.Currency.objects.filter(iso_code="MAD").first(),
    )


CourseLocationFormset = inlineformset_factory(
    models.Course,
    models.CourseLocation,
    form=CourseLocationForm,
    extra=1,
)
