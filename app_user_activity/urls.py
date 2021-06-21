from app_user_activity import views
from django.urls import path

app_name = 'app_user_activity'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('post/', views.UserPosts, name='post'),
    path('search_user/', views.search_user, name='search_user'),
    path('profile_visit/<username>', views.profile_visit, name='profile_visit'),
    path('follow/<username>', views.Follow, name='follow'),
    path('unfollow/<username>', views.UnFollow, name='unfollow'),
    path('follower_list/<username>', views.FollowerList, name='follower_list'),
    path('following_list/<username>', views.FollowingList, name='following_list'),
    path('comment/<pk>/', views.CommentPost, name='comment'),
    path('like/<pk>/', views.LikePost, name='like'),
    path('liked_people/<pk>/', views.LikedPeople, name='liked_people'),
    path('unlike/<pk>/', views.UnlikePost, name='unlike'),
    # path('new_post/', views.Post, name='new_post'),
]
