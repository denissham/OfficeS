from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    email = models.CharField(max_length=200, default='')
    first_name = models.CharField(max_length=200, default='')
    last_name = models.CharField(max_length=200, default='')
    position = models.CharField(max_length=100, default='')
    date_birth = models.DateField(default='')
    wife_name = models.CharField(max_length=200, default='')
    child_quantity = models.PositiveIntegerField(default=0)
    children_names = models.TextField(default='', blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.email + ('' if self.is_active else ' (disabled)') + self.last_name + self.first_name

    