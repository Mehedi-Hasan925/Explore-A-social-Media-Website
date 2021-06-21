from django.urls import path
from app_login import views

app_name = 'app_login'

urlpatterns = [
    path('', views.sign_up, name='signup'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),

    path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name='activate'),

    #reset Password url start###########
    path('password_reset_email/', views.PasswordResetEmail, name='password_reset_email'),
    path('set_new_password/<user>/', views.SetNewPassword, name='set_new_password'),
    path('reset_password_valid_link/<uidb64>/<token>/', views.ResetPasswordValidLink, name='reset_password_valid_link'),
    #reset Password url start###########
    
    path('add_profile_info/', views.Add_Profile_Info, name='add_profile_info'),
    path('login_info_update/', views.login_info_change, name='login_info_update'),
    path('change_profile_photo/', views.change_profile_pic, name='change_profile_photo'),
    path('profile/', views.profile_page, name='profile'),
]