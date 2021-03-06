__author__ = 'FARID ILHAM Al-Q'

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from Apps.Distribution.customer.models import Company
from captcha.fields import CaptchaField


class RegistrationForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta:
        model = Company
        exclude = ('user',)


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['user']


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=15)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:

            if not user.is_active:
                raise forms.ValidationError('This account is disabled.')
        else:
            raise forms.ValidationError('Username atau Password anda salah ')

        return cleaned_data


