from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserPost(models.Model):
    author = models.ForeignKey(User,on_delete = models.CASCADE, related_name='user_post')
    post_description = models.TextField(blank=True)
    post_image = models.FileField(blank=True,upload_to='post_pic')
    upload_date = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-upload_date',]

    def __str__(self):
        return self.post_description


class Like(models.Model):
    post_liked = models.ForeignKey(UserPost, on_delete=models.CASCADE,related_name='liked_post')
    user_liked = models.ForeignKey(User, on_delete=models.CASCADE,related_name='liker')
    liked_date = models.DateTimeField(auto_now_add=True)



class comment(models.Model):
    post_comment = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='blog_comments')
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    comment_content = models.TextField(verbose_name="Comment Here")
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-comment_date',]
        
    def __str__(self):
        return self.comment_content


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_user')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_user')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date',]

