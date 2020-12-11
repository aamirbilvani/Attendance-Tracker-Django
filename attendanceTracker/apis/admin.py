from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin  as BaseUserAdmin 
from .models import AttendanceUser, Office,Attendance,Crash,Analytics
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django import forms




class OfficeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,{'fields': ['name','lat','lng','isactive','create_date','modified_date']}), 
    ]  



class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ('action','search_params','app_version','platform','brand','device','device_model','user')
    fieldsets = [
        (None,{'fields': ['action','search_params','app_version','platform','brand','device','device_model','user']}), 
    ]  




class CrashAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,{'fields': ['exception','app_version','platform','brand','device','device_model','isactive','create_date','modified_date']}), 
    ]  



class AttendanceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,{'fields': ['date','time','lat','lng','ispresent','user','isactive','create_date','modified_date']}), 
    ]  




class AttendanceUserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = AttendanceUser
        fields = ('username', 'fullname','phone','office')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class AttendanceUserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = AttendanceUser
        fields = ('username', 'fullname','phone','office')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = AttendanceUserChangeForm
    add_form = AttendanceUserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'fullname','phone','office')
    list_filter = ('office',)
    fieldsets = (
        (None, {'fields': ('username', 'password','isactive','create_date','modified_date')}),
        ('Personal info', {'fields': ('fullname','phone','office')}),
        ('Analytics', {'fields': ('app_version', 'platform', 'brand', 'device', 'device_model')})
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'fullname','phone','office','password1','password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()



admin.site.register(Office,OfficeAdmin)  
admin.site.register(AttendanceUser, UserAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Crash, CrashAdmin)
admin.site.register(Analytics, AnalyticsAdmin)


