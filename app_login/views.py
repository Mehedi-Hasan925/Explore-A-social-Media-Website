from django.shortcuts import render,HttpResponseRedirect,redirect
from app_login import forms
from app_login import models
from app_user_activity import views
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse,reverse_lazy
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UserChangeForm,PasswordChangeForm
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView,DetailView
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.contrib import messages
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import generate_token
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Create your views here.
def sign_up(request):
    form = forms.SignupForm()
    has_error = False
    if request.method == 'POST':
        form = forms.SignupForm(data=request.POST)
        if form.is_valid():
            email_acc = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')

            if User.objects.filter(username=username).exists():
                messages.add_message(request,messages.ERROR,'This Username have already taken. Choose a new one.')
                has_error = True

            if User.objects.filter(email=email_acc).exists():
                messages.add_message(request,messages.ERROR,'This Email have already taken.')
                has_error = True

            if has_error:
                diction = {'has_error':has_error,'form':form}
                return render(request,'app_login/signup.html',context=diction)
            
            else:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                user_profile = models.UserProfile(user=user)
                user_profile.save()
                messages.add_message(request,messages.SUCCESS,'Check your Email to activate account!')
                # create doamin
                #relative url to verification
                #encode uid 
                #token
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = generate_token.make_token(user)
                domain = get_current_site(request).domain
                relative_url = reverse('app_login:activate',kwargs={'uidb64':uidb64,'token':token})
                # activate_url ='https://'+domain+relative_url
                activate_url ='http://'+domain+relative_url

                email_body = "Hello"+" "+user.first_name + " "+ user.last_name + ", "+ "Follow the below link to verify your Explore account\n" + activate_url
                email_subject = 'Account activation from explore'
                # message = render_to_string('authentication_app/activate.html',
                # {
                #     'user':user,
                #     'domain':domain,
                #     'uidb64':uidb64,
                #     'token':token
                # }
                # )
                email_message = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [email_acc],
                )
                email_message.send()
                HttpResponseRedirect(reverse('app_login:signup'))
            
    diction = {'form':form,'has_error':has_error}
    return render(request,'app_login/signup.html',context=diction)


class ActivateView(View):
    def get(self,request,uidb64,token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        
        except Exception as identifier:
            user=None
        
        if user is not None and generate_token.check_token(user,token):
            user.is_active = True
            user.save()
            messages.add_message(request,messages.INFO, 'Congratualations! Account activated successfully')
            return redirect('app_login:login')
        
        return render(request,'app_login/activate_fail.html')


def log_in(request):
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user =  authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('app_user_activity:home'))

    diction = {'form':form}
    return render(request,'app_login/log_in.html',context=diction)


@login_required
def log_out(request):
    logout(request)
    messages.add_message(request,messages.INFO, 'Logout successfully')
    return HttpResponseRedirect(reverse('app_login:login'))

def PasswordResetEmail(request):
    form = forms.ResetPasswordForm()
    # form = forms.SetNewPassword(request.user)
    # form = forms.ChangePasswordForm(request.user)
    # form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = forms.ResetPasswordForm(data=request.POST)
        if form.is_valid():
            email_acc = form.cleaned_data.get('email')
            user = User.objects.filter(email = email_acc)
            print(email_acc)
            if user.exists():
                # create doamin
                #relative url to verification
                #encode uid 
                #token
                uidb64 = urlsafe_base64_encode(force_bytes(user[0].pk))
                token = PasswordResetTokenGenerator().make_token(user[0])
                domain = get_current_site(request).domain
                relative_url = reverse('app_login:reset_password_valid_link', kwargs={'uidb64':uidb64,'token':token})
                # activate_url ='https://'+domain+relative_url
                activate_url ='http://'+domain+relative_url

                email_body = "Hello"+", \n" +"Your username is "+user[0].username + "\nFollow the below link to Reset your Explore account Password\n" + activate_url
                email_subject = 'Reset Your Password'
                email_message = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [email_acc],
                )
                email_message.send()
                messages.add_message(request,messages.SUCCESS,'Check your Email to Reset Password')
                HttpResponseRedirect(reverse('app_login:password_reset_email'))

            else:
                messages.add_message(request,messages.SUCCESS,'Check your Email to Reset Password')
                HttpResponseRedirect(reverse('app_login:signup'))
                
    diction = {'form':form}
    return render(request,'app_login/password_reset_email.html',context=diction)



def ResetPasswordValidLink(request,uidb64,token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    if PasswordResetTokenGenerator().check_token(user,token):
        return HttpResponseRedirect(reverse('app_login:set_new_password', kwargs={'user':user}))

    return render(request,'app_login/activate_fail.html')


def SetNewPassword(request,user):
    user = User.objects.filter(username=user)
    form = forms.SetNewPassword(user[0])
    if request.method == 'POST':
        form = forms.SetNewPassword(user[0],request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Password reset Successfully! Please Log in')
            return HttpResponseRedirect(reverse('app_login:login'))
        
        else:
            print('form is invalid')

    diction = {'form':form}
    return render(request,'app_login/set_new_password.html',context=diction)

@login_required
def profile_page(request):
    
    return render(request,'app_login/profile.html')




@login_required
def Add_Profile_Info(request):
    current_user = models.UserProfile.objects.get(user=request.user)
    form = forms.UserProfileForm(instance=current_user)
    if request.method == 'POST':
        form = forms.UserProfileForm(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save(commit=True)
            form = forms.UserProfileForm(instance=current_user)
            return HttpResponseRedirect(reverse('app_login:profile'))

    diction = {'form':form}
    return render(request,'app_login/profile_info_set.html',context=diction)

@login_required
def change_profile_pic(request):
    current_user = models.UserProfile.objects.get(user=request.user)
    form = forms.ProfilePicChange(instance=current_user)
    if request.method == 'POST':
        form = forms.ProfilePicChange(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save(commit=True)
            form = forms.ProfilePicChange(instance=current_user)
            return HttpResponseRedirect(reverse('app_login:profile'))

    diction = {'form':form}
    return render(request,'app_login/profile_info_set.html',context=diction)


@login_required
def login_info_change(request):
    current_user = request.user
    form = forms.InformationChangeForm(instance=current_user)
    if request.method == 'POST':
        form = forms.InformationChangeForm(request.POST, instance=current_user)
        if form.is_valid():
            form.save(commit=True)
            form = forms.InformationChangeForm(instance=current_user)
            HttpResponseRedirect(reverse('app_login:profile'))

    diction = {'form':form}
    return render(request,'app_login/login_info_update.html',context=diction)
