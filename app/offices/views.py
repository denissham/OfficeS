

from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Profile, Event, Project
from .forms import LoginForm, UserCreateForm, UserEditForm, ProfileEditForm, EventCreateForm, ProjectCreateForm

# Create your views here.
@login_required
def dashboard(request):
    users = User.objects.filter(is_active=True)
    print(dict(request.session))
    # print(users)
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
    if request.user.is_superuser:
        if request.method == 'POST':
            user_form = UserCreateForm(request.POST)
            if user_form.is_valid():
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data["password"])
                new_user.save()
                Profile.objects.create(user=new_user)
                return render(request, 'offices/dashboard.html',{'new_user':new_user})
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
        profile = Profile.objects.get(user=user)

        return render(request, 'offices/profile.html', locals())
    except:
        messages.error(request, 'Profile data is not filled')
        return render(request, 'offices/profile.html', locals())

@login_required(login_url='../../')
def edit(request, id):
    user = request.user
    user_to_edit = User.objects.get(id=id)
    profile = Profile.objects.get(user=user_to_edit)
    print(user_to_edit)
    print(profile.user)
    if request.method == 'POST':
        form_user = UserEditForm(request.POST)
        form_profile = ProfileEditForm(request.POST)
        
        if user.is_superuser:
            if form_user.is_valid and form_profile.is_valid:
                user_to_edit.first_name = request.POST["first_name"]
                user_to_edit.last_name = request.POST["last_name"]
                user_to_edit.email = request.POST["email"]
                profile.position = request.POST["position"]
                if profile.project_fk:
                    profile.project_fk = request.POST["project_fk"]
                else:
                    profile.project_fk = None
                profile.is_manager = 'is_manager' in request.POST and request.POST['is_manager']
                print(profile.is_manager)
                if profile.is_manager == "on":
                    profile.is_manager = True
                print(profile.is_manager)
                profile.date_of_birth = request.POST["date_of_birth"]
                profile.photo = request.POST["photo"]
                print(profile.photo)
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
                                 'date_of_birth': profile.date_of_birth,'address':profile.address,
                                 'phone':profile.phone, 'child_quantity':profile.child_quantity,
                                  'date_of_start':profile.date_of_start, 'date_of_finish':profile.date_of_finish})
        return render(request, 'offices/edit.html',{'form_user':form_user,'form_profile':form_profile})

@login_required(login_url='../../')
def create_event(request):
    user = request.user
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
    if request.method == 'POST':
        form_project = ProjectCreateForm(request.POST)
        if user.is_superuser:
            if form_project.is_valid:
                new_project = form_project.save(commit=False)
                if new_project.is_manager == "on":
                    new_project.is_manager = True
                new_project.save()
                messages.success(request, "New Project created successfully")
                return redirect('../../')
    else:
        form_project = ProjectCreateForm()
        return render(request,'offices/create_project.html',{'form_project':form_project})
    
@login_required
def projects_list(request):
    user = request.user
    if user.is_superuser:
        projects = Project.objects.filter(is_active=True)
    # print(dict(request.session))
    # print(users)
    return render(request,
              'offices/projects_list.html',
             )