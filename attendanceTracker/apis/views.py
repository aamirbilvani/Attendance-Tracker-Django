from django.shortcuts import render

from django.views import generic

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets 
from rest_framework.decorators import api_view, permission_classes

from .models import Office,AttendanceUser,Attendance
from django.core import serializers
from .serializers import OfficeSerializer,UserSerializer,AttendanceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
 
 
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
    queryset = Office.objects.all().order_by('name')
    serialized=OfficeSerializer(queryset,many=True)   
    response={'response':{'msg':'success','status':200,'data':serialized.data}} 
    return Response(response, status=status.HTTP_200_OK) 
    
    
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getattendance(request): 
    queryset = Attendance.objects.all()
    serialized=AttendanceSerializer(queryset,many=True)   
    response={'response':{'msg':'success','status':200,'data':serialized.data}} 
    return Response(response, status=status.HTTP_200_OK) 



@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_attendance(request):
    serialized = AttendanceSerializer(data=request.data)
    if serialized.is_valid():
        theuser=AttendanceUser.objects.get(pk=serialized.data['user']) 
        attendance = Attendance.objects.create(
            date=serialized.data['date'],
            time=serialized.data['time'],
            lat=serialized.data['lat'],
            lng=serialized.data['lng'],
            ispresent=serialized.data['ispresent'],
            user=theuser,
        ) 
       
        response={'response':{'msg':'success','status':200,'data':serialized.data}} 
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
            office=serialized.data['office']
        )
         
        token=Token.objects.create(user=newuser)
        data={
            'user_id':newuser.id,
            'username':newuser.username,
            'fullname':newuser.fullname,
            'phone':newuser.phone,
            'office':newuser.office.id,
            'token':token.key
            }

        response={'response':{'msg':'success','status':200,'data':data}} 
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class login(ObtainAuthToken): 
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
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
            'token': token.key,
            }
        }
        })
