from django import forms
from apps.courses import models


class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        exclude = ["professor"]


class CourseSearchForm(forms.Form):
    city = forms.ModelChoiceField(models.City.objects)
    area = forms.ModelChoiceField(models.CourseArea.objects)
