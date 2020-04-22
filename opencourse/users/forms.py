from django.contrib.auth import get_user_model, forms

User = get_user_model()


class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
