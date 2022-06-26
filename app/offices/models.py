import datetime

from django.db import models
from django.conf import settings
from phone_field import PhoneField
from django.urls import reverse
from django.core.validators import MinValueValidator

class Project(models.Model):
    name = models.CharField(max_length=200,default='')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.CharField(max_length=200,default='')
    project_fk = models.ForeignKey(Project, on_delete=models.CASCADE, default=None, null=True)
    is_manager = models.BooleanField(default=False)
    date_of_birth = models.DateField(blank=True,null=True)
    photo = models.CharField(max_length=200,default='')
    address = models.CharField(max_length=200,default='')
    phone = PhoneField(blank=True, help_text='Contact phone number')
    married = models.BooleanField(default=False)
    child_quantity = models.IntegerField(default=0)
    date_of_start = models.DateField(blank=True,null=True)
    date_of_finish = models.DateField(blank=True,null=True)

    def __str__(self):
        return f'Profile for user {self.user.first_name} {self.user.last_name}'

class Event(models.Model):
    STATUS = (
       ('rejected', ('Rejected')),
       ('accepted', ('Accepted')),
       ('in_review', ('Created')),
   )
    TYPE = (
       ('vacation', ('Vacation')),
       ('sick_leave', ('Sick leave')),
   )

    type = models.CharField(max_length=32, choices=TYPE)
    description = models.TextField(null=True)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=datetime.date.today)
    user_fk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, related_name='%(class)s_user')
    status = models.CharField(max_length=32,default='In_review', choices=STATUS)
    approve_description = models.TextField(null=True)

class OfficialDays(models.Model):
    year = models.IntegerField(('year'), validators=[MinValueValidator(1984)])
    new_year = models.DateField(blank=True,null=True)
    christmas = models.DateField(blank=True,null=True)
    women_day = models.DateField(blank=True,null=True)
    easter = models.DateField(blank=True,null=True)
    labor_day = models.DateField(blank=True,null=True)
    victory_day = models.DateField(blank=True,null=True)
    trinity = models.DateField(blank=True,null=True)
    constitution_day = models.DateField(blank=True,null=True)
    independence_day = models.DateField(blank=True,null=True)
    defenders_day = models.DateField(blank=True,null=True)
    сatholic_сhristmas = models.DateField(blank=True,null=True)