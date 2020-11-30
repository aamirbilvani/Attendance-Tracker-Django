from django.urls import path

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from . import views
 
app_name = 'apis'
urlpatterns = [ 
    path('', views.IndexView.as_view(), name='index'),
    path('officeapi/', views.OfficeViewSet.as_view({'get':'list','post': 'create'}), name='officeapi'), 
    path('attendanceapi/', views.AttendanceViewSet.as_view({'get':'list','post': 'create'}), name='attendanceapi'), 
    path('getoffices/', views.getoffices, name='getoffices'), 
    path('getattendance/', views.getattendance, name='getattendance'), 
    
    path('register/', views.register, name='registerapi'),
    path('add_attendance/', views.add_attendance, name='add_attendanceapi'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('login/', views.login.as_view(), name='login'),
]
