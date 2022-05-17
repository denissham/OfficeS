from email.policy import default
from django.db import models
from django.conf import settings
from phone_field import PhoneField

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.CharField(max_length=200,default='')
    project = models.CharField(max_length=200,default='')
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
        return f'Profile for user {self.user.username}'