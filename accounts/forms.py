from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.contrib.auth.forms import PasswordResetForm
import re


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ("username", "email")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if len(password1 and password2) < 8:
            raise ValidationError("Password is too short, should be at least 8 characters long.")
        if not re.search(r"[a-z]", password1 and password2):
            raise ValidationError("Password should contain at least one lowercase letter.")
        if not re.search(r"[A-Z]", password1 and password2):
            raise ValidationError("Password should contain at least one uppercase letter.")
        if not re.search(r"[0-9]", password1 and password2):
            raise ValidationError("Password should contain at least one uppercase letter.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1 and password2):
            raise ValidationError("Password should contain at least one special character.")
        if password1 and password2 and password2 != password1:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = "__all__"

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")