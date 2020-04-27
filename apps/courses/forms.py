from django import forms
from apps.courses import models


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
            # "location",
        ]


class CourseSearchForm(forms.Form):
    city = forms.ModelChoiceField(models.City.objects, empty_label="Select City")
    area = forms.ModelChoiceField(models.CourseArea.objects, empty_label="Select Area")
