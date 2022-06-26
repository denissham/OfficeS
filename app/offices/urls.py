from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
   # path('login/', views.user_login, name='login') 
   path('', views.dashboard, name='dashboard'),
   path('login/', auth_views.LoginView.as_view(), name='login'),
   path('logout/', auth_views.LogoutView.as_view(), name="logout"),
   
   path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
   path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

   path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
   path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
   path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

   path('create/', views.create_user, name='create_user'),
   path('profile/<int:id>/', views.profile_detail, name='profile_detail'),
   path('profile/edit/<int:id>/', views.edit, name='edit'),
   
   path('new_event/', views.create_event, name='create_event'),
   path('new_project/', views.create_project, name='create_project'),
   path('projects/', views.projects_list, name='projects'),
   path('events_to_review/', views.in_review_requests, name='events_to_review'),
   path('event/<int:id>/', views.event, name='event'),
   path('event/approve/<int:id>', views.approve_event, name='approve'),
   # path('event/reject/<int:id>', views.reject_event, name='reject'),
   path('next_calendar/<last_day>/', views.next_calendar, name='next_calendar'),
   path('last_calendar/<first_day>', views.last_calendar, name='last_calendar'),
   path('<filter_value>', views.filter_by_team, name='filter_by_team')
]