from dataclasses import fields
from urllib import request
from django import forms
from django.forms import ModelForm
from .models import Profile, Event, Project
from django.contrib.auth.models import User
from django.forms.widgets import NumberInput

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
    email = forms.EmailField()

class ProfileEditForm(forms.ModelForm):
    position = forms.CharField(max_length=200, widget=forms.TextInput())
    project_fk = forms.ModelChoiceField(queryset=Project.objects.filter(is_active = True), required=False)
    is_manager = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    date_of_birth = forms.DateField(widget=forms.NumberInput(attrs={'type': 'date'}))
    photo = forms.CharField(max_length=200, widget=forms.TextInput(), required=False)
    address = forms.CharField(max_length=1024, widget=forms.Textarea())
    phone = forms.NumberInput()
    child_quantity = forms.IntegerField(widget=forms.NumberInput())
    date_of_start = forms.DateField(widget=forms.NumberInput(attrs={'type': 'date'}))
    date_of_finish = forms.DateField(widget=forms.NumberInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Profile
        fields = ('position', 'project_fk', 'is_manager', 'date_of_birth','photo','address','phone','child_quantity','date_of_start', 'date_of_finish')
  
class EventCreateForm(ModelForm):
    
    class Meta:
        model = Event
        fields = ('type', 'description', 'start_date', 'end_date')
        widgets = {'start_date':NumberInput(attrs={'type': 'date'}), 'end_date':NumberInput(attrs={'type': 'date'})}

class ProjectCreateForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = ( 'name', 'is_active' )