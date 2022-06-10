
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
import calendar
from dateutil import parser
import json

from .models import Profile, Event, Project
from .forms import *
import datetime

    
def last_calendar(request, first_day):
    user = request.user
    users = User.objects.filter(is_active=True)
    projects = Project.objects.filter(is_active=True)
    print(dict(request.session))
    try:
        profile = Profile.objects.get(user=user.id)
    except:
        pass
    parsed_first_day = parser.parse(first_day)
    today = parsed_first_day.date()
    start_delta = datetime.timedelta(7)
    start_of_week = today - start_delta
    week_dates = [start_of_week + datetime.timedelta(days=i) for i in range(7)]
    
    events = Event.objects.filter()
    events_for_week = []
    user_events = {}
    
    for event in events:
        test_dates = []
        date_generated = [event.start_date + datetime.timedelta(days=x) for x in range(0, (event.end_date - event.start_date).days+1)]
        for date in week_dates:
            if date in date_generated:
                test_dates.append(event.type)
            else:
                test_dates.append(None)
        user_events[event.user_fk] = test_dates
    
    print(events_for_week) 
            
    print(date_generated)  
        
    return render(request,
              'offices/dashboard.html',
                  locals()
             )

def next_calendar(request, last_day):
    user = request.user
    users = User.objects.filter(is_active=True)
    projects = Project.objects.filter(is_active=True)
    print(dict(request.session))
    try:
        profile = Profile.objects.get(user=user.id)
    except:
        pass
    parsed_last_day = parser.parse(last_day)
    today = parsed_last_day.date()
    start_delta = datetime.timedelta(1)
    start_of_week = today + start_delta
    week_dates = [start_of_week + datetime.timedelta(days=i) for i in range(7)]
    
    events = Event.objects.filter()
    events_for_week = []
    user_events = {}
    
    for event in events:
        test_dates = []
        date_generated = [event.start_date + datetime.timedelta(days=x) for x in range(0, (event.end_date - event.start_date).days+1)]
        for date in week_dates:
            if date in date_generated:
                test_dates.append(event.type)
            else:
                test_dates.append(None)
        user_events[event.user_fk] = test_dates
        
    print(events_for_week) 
            
    print(date_generated)  
    return render(request,
              'offices/dashboard.html',
                  locals()
             )
    
def calendar():
        today = datetime.date.today()
        print(today)
        weekday = today.weekday()
        start_delta = datetime.timedelta(days=weekday)
        start_of_week = today - start_delta
        week_dates = [start_of_week + datetime.timedelta(days=i) for i in range(7)]
        return week_dates
        
@login_required
def dashboard(request):
    user = request.user
    users = User.objects.filter(is_active=True)
    projects = Project.objects.filter(is_active=True)
    week_dates = calendar()
    try:
        profile = Profile.objects.get(user=user.id)
    except:
        pass
    events = Event.objects.filter()
    events_for_week = []
    user_events = {}
    
    for event in events:
        test_dates = []
        date_generated = [event.start_date + datetime.timedelta(days=x) for x in range(0, (event.end_date - event.start_date).days+1)]
        for date in week_dates:
            if date in date_generated:
                test_dates.append(event.type)
            else:
                test_dates.append(None)
        user_events[event.user_fk] = test_dates
    print(user_events)
    print(events_for_week) 
            
    print(date_generated)        
    return render(request,
              'offices/dashboard.html',
                  locals()
             )

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
    user = request.user
    try:
        profile = Profile.objects.get(user=user.id)
    except:
        pass
    if request.user.is_superuser:
        if request.method == 'POST':
            user_form = UserCreateForm(request.POST)
            if user_form.is_valid():
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data["password"])
                new_user.save()
                Profile.objects.create(user=new_user)
                return redirect('/')
            
        else:
            user_form = UserCreateForm()
        return render(request,'offices/create_user.html',{'user_form':user_form})
    
    else:
        return redirect('/offices')

@login_required
def profile_detail(request, id):
    user_me = request.user
    user = get_object_or_404(User, id=id, is_active=True)
    try:
        profile_to_show = Profile.objects.get(user=user)

        return render(request, 'offices/profile.html', locals())
    except:
        messages.error(request, 'Profile data is not filled')
        return render(request, 'offices/profile.html', locals())

@login_required(login_url='../../')
def edit(request, id):
    user = request.user
    user_to_edit = User.objects.get(id=id)
    profile = Profile.objects.get(user=user_to_edit)
    if request.method == 'POST':
        form_user = UserEditForm(request.POST)
        form_profile = ProfileEditForm(request.POST)
        if user.is_superuser:
            if form_user.is_valid and form_profile.is_valid:
                user_to_edit.first_name = request.POST["first_name"]
                user_to_edit.last_name = request.POST["last_name"]
                user_to_edit.email = request.POST["email"]
                profile.position = request.POST["position"]
                if len(form_profile['project_fk'].value()) > 0:
                    project = Project.objects.get(id=form_profile['project_fk'].value())
                    profile.project_fk = project
                else: 
                    profile.project_fk = None
                profile.is_manager = 'is_manager' in request.POST and request.POST['is_manager']
                if profile.is_manager == "on":
                    profile.is_manager = True
                profile.date_of_birth = request.POST["date_of_birth"]
                profile.photo = request.POST["photo"]
                profile.address = request.POST["address"]
                profile.phone = 'phone' in request.POST and request.POST['phone']
                profile.child_quantity = request.POST["child_quantity"]
                profile.date_of_start = request.POST["date_of_start"]
                profile.date_of_finish = request.POST["date_of_finish"]
                user_to_edit.save()
                profile.save()
                url = f'/../profile/{id}'
                messages.success(request, "Data inserted successfully")
                return redirect(url)

        else:
            messages.error(request, 'You are not a superuser')
            return redirect('../../')

    else:
        form_user = UserEditForm(initial={'first_name': user_to_edit.first_name,
                                 'last_name': user_to_edit.last_name,
                                 'email': user_to_edit.email})
        form_profile = ProfileEditForm(initial={'position': profile.position,'user_to_edit': profile.user,
                                 'project_fk': profile.project_fk,'is_manager':profile.is_manager, 
                                 'date_of_birth': profile.date_of_birth,'address':profile.address,'photo':profile.photo,
                                 'phone':profile.phone, 'child_quantity':profile.child_quantity,
                                  'date_of_start':profile.date_of_start, 'date_of_finish':profile.date_of_finish})
        return render(request, 'offices/edit.html',{'form_user':form_user,'form_profile':form_profile})

@login_required(login_url='../../')
def create_event(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user.id)
    except:
        pass
    
    if request.method == 'POST':
        form_event = EventCreateForm(request.POST)
        if form_event.is_valid:
            new_event = form_event.save(commit=False)
            new_event.user_fk = user
            if new_event.type == 'sick_leave':
                new_event.status = 'accepted'
            else:
                new_event.status = 'in_review'
            new_event.save()
            messages.success(request, "New Event created successfully")
            return redirect('../../')
    else:
        form_event = EventCreateForm()
        return render(request,'offices/create_event.html',{'form_event':form_event})

@login_required(login_url='../../')
def create_project(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user.id)
    except:
        pass
    if request.method == 'POST':
        form_project = ProjectCreateForm(request.POST)
        if user.is_superuser:
            if form_project.is_valid:
                new_project = form_project.save(commit=False)
                if new_project.is_active == "on":
                    new_project.is_active = True
                new_project.save()
                messages.success(request, "New Project created successfully")
                return redirect('../../')
    else:
        form_project = ProjectCreateForm()
        return render(request,'offices/create_project.html',{'form_project':form_project})
    
@login_required
def projects_list(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user.id)
    except:
        pass
    if user.is_superuser:
        projects = Project.objects.filter(is_active=True)
    return render(request,
              'offices/projects_list.html', locals()
             )

@login_required(login_url='../../')    
def in_review_requests(request):
    user = request.user
    print(user.id)
    if user.is_superuser:
        test = Event.objects.filter(status = 'in_review')
        print(test)
        return render(request,
              'offices/events_to_review.html', locals()
             )
    else:
        profile = Profile.objects.get(user=user.id)
        if profile.is_manager == True:
            print(profile.project_fk)
            users = Profile.objects.filter(project_fk = profile.project_fk )
            test = 1
            for u in users:
                events_to_show = Event.objects.filter(user_fk = u.id, status = 'in_review' )
                if type(test) == int:
                    test =  events_to_show
                else:
                    test = test | events_to_show
            print(test)
            return render(request,
                'offices/events_to_review.html', locals()
                )
        else:
            messages.error(request, 'You are not a manager')
            return redirect('../../')
            
    
        
@login_required(login_url='../../')
def event(request, id):
    user = request.user
    try:
        profile = Profile.objects.get(user=user.id)
    except:
        pass
    event_to_approve = Event.objects.get(id=id)
    return render(request,
              'offices/event.html', locals()
             )
    
@login_required(login_url='../../')    
def approve_event(request,id):
    user = request.user
    event = Event.objects.get(id=id)
    if user.is_superuser:
        event.status = 'accepted'
        event.save()
        messages.success(request, "Event was successfully approved")
        return HttpResponseRedirect('../../events_to_review/')
    else:
        profile = Profile.objects.get(user=user.id)
        if profile.is_manager == True:
            event.status = 'accepted'
            event.save()
            messages.success(request, "Event was successfully approved")
            return HttpResponseRedirect('../../events_to_review/')
        else:
            messages.error(request, 'You are not a manager')
            return redirect('../../')
            
    
@login_required(login_url='../../')
def reject_event(request,id):
    user = request.user
    event = Event.objects.get(id=id)
    if user.is_superuser:
        event.status = 'rejected'
        event.save()
        messages.success(request, "Event was successfully rejected")
        return HttpResponseRedirect('../../events_to_review/')
    else:
        profile = Profile.objects.get(user=user.id)
        if profile.is_manager == True:
            event.status = 'rejected'
            event.save()
            messages.success(request, "Event was successfully rejected")
            return HttpResponseRedirect('../../events_to_review/')
        else:
            messages.error(request, 'You are not a manager')
            return redirect('../../')

def show_users_by_project(request, project_id):
    
    profiles = Profile.objects.get(project_fk=project_id)
    
    return render(request,
              'offices/dashboard.html',
                  locals()
             )