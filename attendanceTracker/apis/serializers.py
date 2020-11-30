from rest_framework import serializers

from .models import Office, AttendanceUser, Attendance

class OfficeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Office
        fields = ('id','name', 'lat', 'lng')
        
        
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ('id','date', 'time','lat', 'lng','ispresent','user')
          
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttendanceUser 
        fields = ( "username", "password", "fullname", "phone", "office" )
