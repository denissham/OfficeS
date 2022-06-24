from django.contrib.auth.models import User

class EmailAuthBackend(object):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.object.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
            
        except User.DoesNotExist:
            return None