from django.contrib import admin
from .models import Profile, Event, OfficialDays, Project

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'position', 'is_manager', 
                'date_of_birth', 'photo', 'address', 'phone', 'married',
                'child_quantity', 'date_of_start', 'date_of_finish']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['user_fk', 'type', 'description', 'start_date', 'end_date', 
                    'status']

@admin.register(OfficialDays)
class OfficialDaysAdmin(admin.ModelAdmin):
    list_display = ['year', 'new_year', 'christmas', 'women_day', 'easter', 
                    'labor_day','victory_day','trinity','constitution_day','independence_day','сatholic_сhristmas']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']   

    