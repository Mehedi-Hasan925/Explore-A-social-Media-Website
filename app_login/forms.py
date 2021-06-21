from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UserChangeForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from app_login import models

class SignupForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="",widget=forms.TextInput(attrs={'placeholder':'First Name','class':'mb-2'}))
    last_name = forms.CharField(required=True, label="",widget=forms.TextInput(attrs={'placeholder':'Last Name','class':'mb-2'}))
    email = forms.EmailField(required=True, label="",widget=forms.TextInput(attrs={'placeholder':'Email','class':'mb-2'}))
    username = forms.CharField(required=True, label="",widget=forms.TextInput(attrs={'placeholder':'Username','class':'mb-2'}))
    password1 = forms.CharField(required=True, label="",widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'mb-2'}))
    password2 = forms.CharField(required=True, label="",widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password','class':'mb-2'}))
    class Meta:
        model = User
        fields = ('email','first_name','last_name','username','password1','password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, label="",widget=forms.TextInput(attrs={'placeholder':'Username','class':'mb-3'}))
    password = forms.CharField(required=True, label="",widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'mb-3'}))
    class Meta:
        model = User
        fields = ('username','password')

class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(required=True, label="",widget=forms.TextInput(attrs={'placeholder':'Email','class':'mb-2'}))
    class Meta:
        model = User
        fields = ('email',)

class SetNewPassword(SetPasswordForm):
    new_password1 = forms.CharField(required=True, label="",widget=forms.PasswordInput(attrs={'placeholder':'New Password','class':'mb-2'}))
    new_password2 = forms.CharField(required=True, label="",widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password','class':'mb-2'}))
    class Meta:
        model = User
        fields = ('new_password1','new_password2')
    
class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(required=True, label="",widget=forms.PasswordInput(attrs={'placeholder':'Old Password','class':'mb-2'}))
    new_password1 = forms.CharField(required=True, label="",widget=forms.PasswordInput(attrs={'placeholder':'New Password','class':'mb-2'}))
    new_password2 = forms.CharField(required=True, label="",widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password','class':'mb-2'}))
    class Meta:
        model = User
        fields = ('old_password','new_password1','new_password2')


class UserProfileForm(forms.ModelForm):
    school = forms.CharField(label="",required=False,widget=forms.TextInput(attrs={'placeholder':'Enter School Name','class':'mb-3 mt-3'}))
    College = forms.CharField(label="",required=False,widget=forms.TextInput(attrs={'placeholder':'Enter College Name','class':'mb-3'}))
    other_institution = forms.CharField(label="",required=False,widget=forms.TextInput(attrs={'placeholder':'Graduation School','class':'mb-3'}))
    training = forms.CharField(label="",required=False,widget=forms.TextInput(attrs={'placeholder':'If you have any training','class':'mb-3'}))
    dob = forms.DateField(label="Date of Birth", widget=forms.TextInput(attrs={'type':'date','class':'mb-3'}))
    class Meta:
        model = models.UserProfile
        fields = ('profile_pic','school','College','other_institution','training','dob','facebook_id')


class ProfilePicChange(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ('profile_pic',)


class InformationChangeForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ('username','email')