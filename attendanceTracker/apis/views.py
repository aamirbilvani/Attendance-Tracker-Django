from django.shortcuts import render

from django.views import generic

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets 
from rest_framework.decorators import api_view, permission_classes

from .models import Office,AttendanceUser,Attendance,Crash,Analytics
from django.core import serializers
from .serializers import OfficeSerializer,UserSerializer,AttendanceSerializer,CrashSerializer,LoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
 
class IndexView(generic.ListView):
    template_name = 'apis/index.html' 
         
class OfficeViewSet(viewsets.ModelViewSet):
    queryset = Office.objects.all().order_by('name')
    serializer_class = OfficeSerializer
    
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    
    
@api_view(['GET'])
def getoffices(request):  
    queryset = Office.objects.filter(isactive=True).order_by('name')
    serialized=OfficeSerializer(queryset,many=True)   
    
    response={'response':{'msg':'success','status':200,'data':serialized.data}} 
    return Response(response, status=status.HTTP_200_OK) 
    
    
    
    
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getattendance(request): 
    queryset = Attendance.objects.filter(isactive=True)
    serialized=AttendanceSerializer(queryset,many=True)   
    response={'response':{'msg':'success','status':200,'data':serialized.data}} 
    return Response(response, status=status.HTTP_200_OK) 



@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_attendance(request):
    serialized = AttendanceSerializer(data=request.data)
    if serialized.is_valid():
        token=request.META['HTTP_AUTHORIZATION'][6:]
        token_instance=Token.objects.get(key=token)
        theuser=AttendanceUser.objects.filter(isactive=True).get(pk=token_instance.user_id)
        attendance = Attendance.objects.create(
            date=serialized.data['date'],
            time=serialized.data['time'],
            lat=serialized.data['lat'],
            lng=serialized.data['lng'],
            ispresent=serialized.data['ispresent'],
            user=theuser,
        ) 
        Analytics.objects.create(action='add_attendance',search_params='',app_version=theuser.app_version,platform=theuser.platform,brand=theuser.brand,device=theuser.device,device_model=theuser.device_model)
     
        response={'response':{'msg':'success','status':200,'data':serialized.data}} 
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def logout(request):  
    
    token=request.META['HTTP_AUTHORIZATION'][6:]
    instance = Token.objects.get(key=token)
    theuser=AttendanceUser.objects.filter(isactive=True).get(pk=instance.user_id)
    instance.delete()
    Analytics.objects.create(action='logout',search_params='',app_version=theuser.app_version,platform=theuser.platform,brand=theuser.brand,device=theuser.device,device_model=theuser.device_model)
    
    response={'response':{'msg':'success','status':200}} 
    return Response(response, status=status.HTTP_200_OK) 
    
@api_view(['POST'])
def add_crash(request):   
    serialized = CrashSerializer(data=request.data)
    if serialized.is_valid():
        Crash.objects.create(
            exception=serialized.data['exception'],
            app_version=serialized.data['app_version'],
            platform=serialized.data['platform'],
            brand=serialized.data['brand'],
            device=serialized.data['device'],
            device_model=serialized.data['device_model']
        )
        response={'response':{'msg':'success','status':200}}
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
def register(request):
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        newuser=AttendanceUser.objects.create_user(
            serialized.data['username'],
            password=serialized.data['password'],
            fullname=serialized.data['fullname'],
            phone=serialized.data['phone'],
            office=serialized.data['office'],
            app_version=serialized.data['app_version'],
            platform=serialized.data['platform'],
            brand=serialized.data['brand'],
            device=serialized.data['device'],
            device_model=serialized.data['device_model'],
        )
        Analytics.objects.create(action='register',search_params='',app_version=serialized.data['app_version'],platform=serialized.data['platform'],brand=serialized.data['brand'],device=serialized.data['device'],device_model=serialized.data['device_model'])
        
        token=Token.objects.create(user=newuser)
        
        data={
            'user_id':newuser.id,
            'username':newuser.username,
            'fullname':newuser.fullname,
            'phone':newuser.phone,
            'office_id':newuser.office.id,
            'office_name':newuser.office.name,
            'token':token.key
            }

        response={'response':{'msg':'success','status':200,'data':data}} 
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
        
        
         
        
class login(ObtainAuthToken):
    def post(self, request, format=None):
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)
        app_version = data.get('app_version', None)
        platform= data.get('platform', None)
        brand= data.get('brand', None)
        device= data.get('device', None)
        device_model= data.get('device_model', None)
        
        user = authenticate(username=username, password=password)
        
        user.app_version=app_version
        user.platform=platform
        user.brand=brand
        user.device=device
        user.device_model=device_model
        user.save()
        
        Analytics.objects.create(action='login',search_params='',app_version=app_version,platform=platform,brand=brand,device=device,device_model=device_model)
        
        if user is not None:
            if user.isactive==True:
                token, created = Token.objects.get_or_create(user=user)
                
                return Response(
                {
                'response':
                {
                    'msg':'success',
                    'status':200,
                    'data':{
                    'user_id': user.pk,
                    'username': user.username,
                    'fullname': user.fullname,
                    'phone': user.phone,
                    'office_id': user.office.id, 
                    'office_name':user.office.name,
                    'token': token.key, 
                    }
                }
                })
                
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
