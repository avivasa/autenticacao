from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")


class ChangePasswordForm(PasswordChangeForm):
    new_password1 = forms.CharField(label="Nova senha", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirmação da nova senha", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 != new_password2:
            raise forms.ValidationError("As senhas não correspondem. Por favor, tente novamente.")

        return cleaned_data
