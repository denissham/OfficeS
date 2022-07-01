from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.forms.widgets import NumberInput
from django.core.validators import MinLengthValidator

from .models import Profile, Event, Project


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput, validators=[MinLengthValidator(8, 
        message="Ensure this value has at least %(limit_value)d character (it has ""%(show_value)d).")])
    first_name = forms.CharField(required=True, max_length=150)
    last_name = forms.CharField(required=True, max_length=150)
    email = forms.CharField(required=True, max_length=150)
    username = forms.CharField(required=True, max_length=50)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class UserEditForm(forms.Form):

    first_name = forms.CharField(max_length=150, widget=forms.TextInput())
    last_name = forms.CharField(max_length=150, widget=forms.TextInput())
    email = forms.EmailField()


class ProfileEditForm(ModelForm):
    position = forms.CharField(max_length=200, widget=forms.TextInput())
    project_fk = forms.ModelChoiceField(queryset=Project.objects.filter(is_active = True), required=False)
    is_manager = forms.BooleanField(required=False, widget=forms.CheckboxInput(),label=("Manager’s access"))
    date_of_birth = forms.DateField(widget=forms.NumberInput(attrs={'type': 'date'}), label=("Date of birth"))
    address = forms.CharField(max_length=1024, widget=forms.Textarea())
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'number','placeholder':('Phone')}), label=("Phone number"),
                               required=False)
    child_quantity = forms.IntegerField(widget=forms.NumberInput(), min_value=0)
    date_of_start = forms.DateField(widget=forms.NumberInput(attrs={'type': 'date'}))
    date_of_finish = forms.DateField(widget=forms.NumberInput(attrs={'type': 'date'}), required=False)
    
    class Meta:
        model = Profile
        fields = ('position', 'project_fk', 'is_manager', 'date_of_birth', 'address', 'phone','child_quantity','date_of_start', 'date_of_finish')
    
    
class EventCreateForm(ModelForm):
    
    class Meta:
        model = Event
        fields = ('type', 'description', 'start_date', 'end_date')
        widgets = {'start_date':NumberInput(attrs={'type': 'date'}), 'end_date':NumberInput(attrs={'type': 'date'})}

    def clean(self):
        cleaned_data = super(EventCreateForm, self).clean()
        from_time = cleaned_data.get("start_date")
        end_time = cleaned_data.get("end_date")

        if from_time and end_time:
            if end_time < from_time:
                raise forms.ValidationError("End date cannot be earlier than start date!")
        return cleaned_data
    
class ProjectCreateForm(forms.ModelForm):
    is_active = forms.BooleanField(required=True, widget=forms.CheckboxInput(),label=("Active"))
    class Meta:
        model = Project
        fields = ( 'name', 'is_active' )
        
class EventApproveForm(ModelForm):
    
    class Meta:
        model = Event
        fields = ( 'approve_description',)
               
        