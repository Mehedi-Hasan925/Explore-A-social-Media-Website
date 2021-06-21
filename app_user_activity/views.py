from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
from app_user_activity import models
from app_user_activity import forms
from django.contrib.auth.models import User
from django.views.generic import CreateView,DetailView,DeleteView,UpdateView
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse,reverse_lazy
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.db.models import Q

import app_user_activity


# Create your views here.
@login_required
def home(request):
    following_list = models.Follow.objects.filter(follower=request.user)
    posts = models.UserPost.objects.filter(author__in=following_list.values_list('following'))
    liked_post = models.Like.objects.filter(user_liked=request.user)
    liked_post_list = liked_post.values_list('post_liked',flat=True)
    diction = {'posts':posts,'liked_post_list':liked_post_list}
    return render(request,'app_user_activity/home.html',context=diction)


@login_required
def UserPosts(request):
    form = forms.UserPostForm()
    if request.method == 'POST':
        form = forms.UserPostForm(request.POST, request.FILES)
        if form.is_valid():
            data_form = form.save(commit=False)
            data_form.author = request.user
            data_form.save()
            return HttpResponseRedirect(reverse('app_user_activity:home'))

    diction = {'form':form}
    return render(request,'app_user_activity/user_posts.html',context=diction)


@login_required
def Follow(request,username):
    follower_user = request.user
    following_user = User.objects.get(username=username)
    already_followed = models.Follow.objects.filter(follower=follower_user, following=following_user)

    if not already_followed:
        followed_user = models.Follow(follower=follower_user,following=following_user)
        followed_user.save()

    return HttpResponseRedirect(reverse('app_user_activity:profile_visit',kwargs={'username':username}))


@login_required
def UnFollow(request,username):
    follower_user = request.user
    following_user = User.objects.get(username=username)
    already_followed = models.Follow.objects.filter(follower=follower_user, following=following_user)
    already_followed.delete()
    return HttpResponseRedirect(reverse('app_user_activity:profile_visit',kwargs={'username':username}))



@login_required
def profile_visit(request,username):
    already_followed = False
    visited_user = User.objects.get(username=username)
    if models.Follow.objects.filter(follower=request.user,following=visited_user).exists():
        already_followed =True
    diction = {'visited_user':visited_user,'already_followed':already_followed}
    return render(request,'app_user_activity/profile_visit.html',context=diction)


@login_required
def search_user(request):
      if request.method == 'GET':
        pattern = request.GET.get('search','')
        result = User.objects.filter(Q(username__icontains=pattern) | Q(first_name__icontains=pattern) | Q(last_name__icontains=pattern))
        diction = {'result':result,'pattern':pattern}
        return render(request,'app_user_activity/search_user.html',context=diction)


@login_required
def FollowerList(request,username):
    current_user = User.objects.get(username=username)
    my_follower = models.Follow.objects.filter(following=current_user)
    follower_objects=[]
    for i in my_follower:
        follower_objects.append(i.follower)
    diction = {'follower_objects':follower_objects}
    return render(request,'app_user_activity/follower_list.html',context=diction)


@login_required
def FollowingList(request,username):
    current_user = User.objects.get(username=username)
    my_following = models.Follow.objects.filter(follower=current_user)
    following_objects=[]
    for i in my_following:
        following_objects.append(i.following)
    diction = {'following_objects':following_objects}
    return render(request,'app_user_activity/following_list.html',context=diction)

@login_required
def LikePost(request,pk):
    post = models.UserPost.objects.get(pk=pk)
    already_liked = models.Like.objects.filter(post_liked=post, user_liked=request.user)
    if not already_liked:
        liked_post = models.Like(post_liked=post, user_liked=request.user)
        liked_post.save()
    
    return HttpResponseRedirect(reverse('app_user_activity:home'))


@login_required
def UnlikePost(request,pk):
    post = models.UserPost.objects.get(pk=pk)
    already_liked = models.Like.objects.filter(post_liked=post, user_liked=request.user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('app_user_activity:home'))


@login_required
def CommentPost(request,pk):
    comment_form = forms.CommentForm()
    commented_post = models.UserPost(pk=pk)
    if request.method == 'POST':
        comment_form = forms.CommentForm(request.POST)
        if comment_form.is_valid():
            data_form=comment_form.save(commit=False)
            data_form.post_comment = commented_post
            data_form.user_comment = request.user
            data_form.save()
            return HttpResponseRedirect(reverse('app_user_activity:home'))
    diction={'comment_form':comment_form}
    return render(request,'app_user_activity/comment_form.html',context=diction)

@login_required
def LikedPeople(request,pk):
    posts = models.UserPost.objects.get(pk=pk)
    liked_user = models.Like.objects.filter(post_liked=posts)
    diction = {'liked_user':liked_user}
    return render(request,'app_user_activity/liked_people.html',context=diction)