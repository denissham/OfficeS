from django.urls import path
from . import views

from .views import dashboard

urlpatterns = [
    path('',views.home),
    path('dashboard/', dashboard, name='dashboard'),
]