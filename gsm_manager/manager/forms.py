from django import forms
from django.contrib.auth.models import User
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', required=True)
    password = forms.CharField(label='Пароль', required=True, widget=forms.PasswordInput)

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Логин', required=True)
    email = forms.CharField(label='Email', required=True)
    first_name = forms.CharField(label='Имя', required=True)
    last_name = forms.CharField(label='Фамилия', required=True)
    password = forms.CharField(label='Пароль', required=True, widget=forms.PasswordInput)

class UserEditForm(forms.Form):
    username = forms.CharField(label='Логин', required=True)
    email = forms.CharField(label='Email', required=True)
    first_name = forms.CharField(label='Имя', required=True)
    last_name = forms.CharField(label='Фамилия', required=True)
    old_password = forms.CharField(label='Старый пароль', required=True, widget=forms.PasswordInput)
    new_password = forms.CharField(label='Новый пароль', required=True, widget=forms.PasswordInput)

class DeviceRegistrationForm(forms.Form):
    serial_number = forms.CharField(label='Серийный номер', required=True)
    name = forms.CharField(label='Название', required=True)
    description = forms.CharField(label='Описание', widget=forms.Textarea)

class DeviceEditForm(forms.Form):
    name = forms.CharField(label='Название', required=True)
    description = forms.CharField(label='Описание', widget=forms.Textarea)

class DeviceConfigForm(forms.Form):
    active = forms.BooleanField(label='Активность', required=False)
    alarmTime = forms.CharField(label='Время до срабатывания тревоги', required=True)
    id = forms.CharField(label='Серийный номер', required=True)
    phone = forms.CharField(label='Телефон', required=True)
    smsText = forms.CharField(label='Текст SMS сообщения', required=True)
    name = forms.CharField(label='Название', required=True)