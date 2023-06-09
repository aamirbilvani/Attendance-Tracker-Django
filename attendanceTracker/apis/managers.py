from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

from . import models

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username, password,fullname,phone,office,app_version,platform,brand,device,device_model):
        """
        Create and save a User with the given email and password.
        """
        if not username:
            raise ValueError(_('The username must be set')) 
        user = self.model(username=username,fullname=fullname,phone=phone,office=models.Office.objects.get(pk=office),app_version=app_version,platform=platform,brand=brand,device=device,device_model=device_model)
        user.set_password(password)
        user.save() 
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)
