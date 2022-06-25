from .models import Profile

def save_profile(backend, user, response, *args, **kwargs):
    
    if backend.name == 'google-oauth2':
        try:
            profile = Profile.objects.get(user=user)
            profile.photo = response['picture'] 
            print(response['picture'])
            profile.save()
        except:
            Profile.objects.create(user=user)
            profile = Profile.objects.get(user=user)
            profile.photo = response['picture']
            profile.save()
