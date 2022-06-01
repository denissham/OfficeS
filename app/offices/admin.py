from django.contrib import admin
from .models import Profile, Event

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'position', 'is_manager', 
                'date_of_birth', 'photo', 'address', 'phone', 'married',
                'child_quantity', 'date_of_start', 'date_of_finish']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['user_fk', 'type', 'description', 'start_date', 'end_date', 
                    'status']

