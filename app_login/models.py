from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    profile_pic = models.ImageField(upload_to='profile_pics',verbose_name='Profile Photo')
    school = models.CharField(max_length=150,blank=True, verbose_name='Add School')
    College = models.CharField(max_length=150, blank=True, verbose_name='Add College')
    other_institution = models.CharField(max_length=250, blank=True, verbose_name='Add institution')
    training = models.CharField(max_length=250, blank=True, verbose_name='Add training(if you have any)')
    dob = models.DateField(blank=True, verbose_name='Date of Birth',null=True)
    facebook_id = models.URLField(blank=True, verbose_name='Facebok Id')

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
