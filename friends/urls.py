from .views import UserProfileView, FollowActionView, UserSearchApiView
from django.urls import path

urlpatterns = [
    path('u/<str:username>/', UserProfileView.as_view(), name='user_profile'),
    path('u/<str:username>/follow/', FollowActionView.as_view(), name='follow_action'),
    path('search/api/', UserSearchApiView.as_view(), name='user_search_api'),
]