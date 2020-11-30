from django.db import models
from django.contrib.auth.models import AbstractUser 

from .managers import CustomUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from datetime import datetime
 
class Office(models.Model):
    name=models.CharField (max_length=50, null=True, default=None, blank=True)
    lat=models.CharField (max_length=50, null=True, default=None, blank=True)
    lng=models.CharField (max_length=50, null=True, default=None, blank=True)
     
    def get_name(self):
        return self.name 
        
    def get_lat(self):
        return self.lat
        
    def get_lng(self):
        return self.lng 
        
    def __str__(self):
        return self.name
        
    class Meta:
      db_table = 'office_mst'  
      ordering = ['id']
      
      


class AttendanceUser(AbstractUser):
    
    fullname=models.CharField (max_length=50, null=True, default=None, blank=True) 
    phone=models.CharField (max_length=50, null=True, default=None, blank=True) 
    office=models.ForeignKey(Office, null=True, on_delete=models.CASCADE)
      
    objects = CustomUserManager()
    
    def get_fullname(self):
        return self.fullname
    def get_phone(self):
        return self.phone 
    def office_id(self):
        return self.user_office.id
    def office_name(self):
        return self.user_office.name 
    class Meta:
      db_table = 'attendance_user_mst'  
      ordering = ['id']
      
      
      
class Attendance(models.Model):
    date=models.DateField (null=True, default=datetime.now().date(), blank=True)
    time=models.TimeField (auto_now=False, auto_now_add=False, default=datetime.now().time(), blank=True)
    lat=models.CharField (max_length=50, null=True, default=None, blank=True) 
    lng=models.CharField (max_length=50, null=True, default=None, blank=True) 
    ispresent=models.BooleanField (null=True, default=None, blank=True) 
    
    user=models.ForeignKey(AttendanceUser, null=True, on_delete=models.CASCADE)
     
    def get_attendance(self):
        return self.ispresent  
        
    def __str__(self):
        return str(self.date) + str(self.time)
    class Meta:
      db_table = 'attendance_mst'  
      ordering = ['id']
       
