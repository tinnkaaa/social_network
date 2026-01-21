from .views import UserProfileView, FollowActionView, UserSearchApiView, FollowersListView, FollowingListView
from django.urls import path

urlpatterns = [
    path('u/<str:username>/', UserProfileView.as_view(), name='user_profile'),
    path('u/<str:username>/follow/', FollowActionView.as_view(), name='follow_action'),
    path('search/api/', UserSearchApiView.as_view(), name='user_search_api'),
    path('u/<str:username>/followers/', FollowersListView.as_view(), name='followers_list'),
    path('u/<str:username>/following/', FollowingListView.as_view(), name='following_list'),
]