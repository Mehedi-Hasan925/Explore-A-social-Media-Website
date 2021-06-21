from django import forms
from app_user_activity import models

# forms here
class UserPostForm(forms.ModelForm):
    # post_description = forms.CharField(required=True, label="",widget=forms.TextInput(attrs={'placeholder':'First Name','class':'mb-2'}))
    # post_image = forms.Textarea(required=True, label="",widget=forms.TextInput(attrs={'placeholder':'Last Name','class':'mb-2'}))
    class Meta:
        model = models.UserPost
        fields = ("post_description","post_image")


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = models.comment
        fields = ("comment_content",)

