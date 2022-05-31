from dataclasses import fields
from urllib import request
from django import forms
from django.forms import ModelForm
from .models import Profile, Event
from django.contrib.auth.models import User
from django.shortcuts import get_list_or_404
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

class ProfileEditForm(forms.Form):
    position = forms.CharField(max_length=200, widget=forms.TextInput())
    project = forms.CharField(max_length=200, widget=forms.TextInput())
    is_manager = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    date_of_birth = forms.DateField(widget=forms.NumberInput(attrs={'type': 'date'}))
    photo = forms.CharField(max_length=200, widget=forms.TextInput(), required=False)
    address = forms.CharField(max_length=1024, widget=forms.Textarea())
    phone = forms.NumberInput()
    child_quantity = forms.IntegerField(widget=forms.NumberInput())
    date_of_start = forms.DateField(widget=forms.NumberInput(attrs={'type': 'date'}))
    date_of_finish = forms.DateField(widget=forms.NumberInput(attrs={'type': 'date'}))

# def _all_managers():
#     users_to_show = []
#     t = Profile.objects.filter(is_manager = True)
#     profiles =[]
#     for item in t:
#         profiles.append(item.user)
#     for k in profiles:
#         if k.is_active == True:
#             tup = (k.first_name +" "+ k.last_name, k.first_name +" "+ k.last_name)
#             users_to_show.append(tup)
#     return users_to_show  


# class EventCreateForm(forms.Form):
#     TYPE = [
#     ('vacation', 'Vacation'),
#     ('sick_leave', 'Sick Leave'),
# ]

#     type = forms.ChoiceField(choices=TYPE)
#     description = forms.CharField(max_length=200, widget=forms.Textarea)
#     start_date = forms.DateField(widget=forms.DateInput(), input_formats=['%Y-%m-%d'], required=False)
#     end_date = forms.DateField(widget=forms.DateInput(), input_formats=['%Y-%m-%d'] ,required=False)
    
    # manager_fk = forms.ModelChoiceField(widget=forms.Select(), choices=_all_managers())
    # manager = forms.MultipleChoiceField(choices=_all_managers())
    # manager_fk = forms.ModelChoiceField(queryset=Profile.objects.get(is_manager = True))
    # manager_two_fk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, related_name='%(class)s_secondapprover')
    # status = models.CharField(max_length=32,default='In_review',
  
  
  
class EventCreateForm(ModelForm):
    
    class Meta:
        model = Event
        fields = ('type', 'description', 'start_date', 'end_date')
        widgets = {'start_date':NumberInput(attrs={'type': 'date'}), 'end_date':NumberInput(attrs={'type': 'date'})}
        # 
        # def save(self, commit=True):
        #     user = super().save(commit=False) # here the object is not commited in db
        #     user.email = self.cleaned_data['username']
        #     user.save()
        #     return user
    # class Meta:
    #     model = TagStatus
    #     fields = ('slug', 'ext')
    #     widgets = {'slug': forms.HiddenInput()}