from django import forms
from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Invalid username or password.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


class UserCreateEmailForm(UserCreationForm):
    email = forms.EmailField(required=False,
                             label='E-mail',
                             widget=forms.EmailInput(attrs={'size': "35", }))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateEmailForm, self).save(commit=False)
        user.email = self.cleaned_data.get("email")
        if commit:
            user.save()
        return user
