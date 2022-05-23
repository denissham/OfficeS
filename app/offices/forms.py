from dataclasses import fields
from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class UserEditForm(forms.Form):

    first_name = forms.CharField(max_length=200, widget=forms.TextInput())
    last_name = forms.CharField(max_length=200, widget=forms.TextInput())
    email = forms.CharField(max_length=200, widget=forms.TextInput())

class ProfileEditForm(forms.Form):
    position = forms.CharField(max_length=200, widget=forms.TextInput())
    project = forms.CharField(max_length=200, widget=forms.TextInput())
    is_manager = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    date_of_birth = forms.DateField(widget=forms.DateInput())
    photo = forms.CharField(max_length=200, widget=forms.TextInput())
    address = forms.CharField(max_length=1024, widget=forms.Textarea())
    phone = forms.NumberInput()
    child_quantity = forms.IntegerField(widget=forms.NumberInput())
    date_of_start = forms.DateField(widget=forms.DateInput())
    date_of_finish = forms.DateField(widget=forms.DateInput())