from django.shortcuts import render
from .models import Profile
from django.contrib.auth.models import User

from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages


def home(request):
    return render(request, 'home.html', {})

def user_login(request):
    user = get_object_or_404(User, pk=user_id)
    if user:
        if user.is_active:
            superusers = User.objects.filter(is_superuser=True)
            if user in superusers:
                request.session['role'] = "superuser"
            else:
                request.session['role'] = "user"
            login(request, user)
            return HttpResponseRedirect('./dashboard', user)
        else:
            messages.error(request, 'You can not login')
            return redirect('/login')

def dashboard(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'offices/dashboard.html', locals())

