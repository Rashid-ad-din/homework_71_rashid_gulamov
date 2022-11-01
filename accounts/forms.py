from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import TextInput


class LoginForm(forms.Form):
    login = forms.CharField(required=True, label='Логин')
    password = forms.CharField(required=True, label='Пароль', widget=forms.PasswordInput)
    next = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = get_user_model()
        fields = ('login', 'password')


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', strip=False, required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Подтвердите пароль', strip=False, required=True,
                                       widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = (
            'login', 'email', 'avatar', 'password', 'password_confirm', 'first_name', 'user_info', 'phone', 'gender')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError('Пароли не совпадают')
        first_name = cleaned_data.get('first_name')
        if not first_name:
            raise ValidationError('Поле "Имя" обязательно к заполнению')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'login', 'email', 'avatar')
        labels = {'first_name': 'Имя', 'login': 'Логин', 'email': 'Email'}


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='', widget=TextInput(attrs={
        'class': 'mr-3 ps-3 class-form border-0 border-top bg-light rounded',
        'style': 'width: 270px; height: 35px; outline:0px none transparent; overflow:auto; resize:none',
        'placeholder': 'Поиск',
    }
    ))
