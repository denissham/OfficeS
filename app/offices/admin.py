from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'position', 'project', 'is_manager', 'date_of_birth', 'photo', 'address', 'phone', 'married',
    'child_quantity', 'date_of_start', 'date_of_finish']