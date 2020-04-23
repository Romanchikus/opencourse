from django import forms
from opencourse.courses import models


class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        exclude = ["professor"]
