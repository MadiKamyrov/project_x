from django.contrib.auth.backends import ModelBackend

from user.models import User


class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        if username is not None:
            email = username
        if email:
            user = User.objects.get(email=email)
        pwd_valid = user.check_password(password)
        if pwd_valid:
            return user
        return None