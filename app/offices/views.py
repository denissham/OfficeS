from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'offices/dashboard.html',{'section':'dashboard'} )

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],
                                        password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('Authenticated'' Successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form=LoginForm()
    return render(request, 'offices/login.html', {'form':form})

@login_required
def create_user(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            user_form = UserCreateForm(request.POST)
            if user_form.is_valid():
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data["password"])
                new_user.save()
                return render(request, 'offices/dashboard.html',{'new_user':new_user})
        else:
            user_form = UserCreateForm()
        return render(request,'offices/create_user.html',{'user_form':user_form})
    else:
        return redirect('/offices')