from rest_framework import serializers

from .models import Office, AttendanceUser, Attendance, Crash

class OfficeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Office
        fields = ('id','name', 'lat', 'lng')
        
        
class CrashSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crash
        fields = ('id','exception', 'app_version', 'platform', 'brand', 'device', 'device_model')
        
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ('id','date', 'time','lat', 'lng','ispresent','user')
          
class UserSerializer(serializers.ModelSerializer): 
    class Meta:
        model = AttendanceUser 
        fields = ("username", "password", "fullname", "phone", "office", "app_version", "platform", "brand", "device", "device_model")
        
        
class LoginSerializer(serializers.ModelSerializer): 
    class Meta:
        model = AttendanceUser 
        fields = ( "username", "password", "app_version", "platform", "brand", "device", "device_model" )
        
        def validate(self, data):
            username = data.get("username", None)
            password = data.get("password", None)
            user = authenticate(username=username, password=password)
            if user is None:
                raise serializers.ValidationError(
                    'A user with this email and password is not found.'
                )
            else:
                return {
                    'email':user.email,
                    'app_version':app_version,
                }
