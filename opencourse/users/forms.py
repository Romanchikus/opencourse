from opencourse.users import models
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_forms

User = get_user_model()


class UserCreationForm(auth_forms.UserCreationForm):
    USER_TYPES = [("student", "student"), ("professor", "professor")]
    user_type = forms.ChoiceField(
        choices=USER_TYPES
    )

    class Meta(auth_forms.UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)

        user_type = self.cleaned_data["user_type"]
        user_type_class_map = {
            "professor": models.Professor,
            "student": models.Student,
        }
        user_class = user_type_class_map[user_type]
        profile = user_class()
        setattr(user, user_type, profile)

        if commit:
            user.save()
            profile.save()
        return user
