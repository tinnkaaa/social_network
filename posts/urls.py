from django.urls import path
from .views import *

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/like/', PostLikeView.as_view(), name='post_like'),
    path('<int:pk>/comment/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
]