from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, rquest, username=None, password=None, **kwargs):
        user = None
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user=None
        
        if user.check_password(password):
            return user
        return None
