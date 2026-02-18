from django.urls import path
from .views import (
    NotificationListView,
    MarkAsReadView,
    MarkAllAsReadView,
    UnreadCountView
)

app_name = 'notifications'

urlpatterns = [
    path('', NotificationListView.as_view(), name='list'),
    path('read/<int:pk>/', MarkAsReadView.as_view(), name='read'),
    path('read-all/', MarkAllAsReadView.as_view(), name='read_all'),
    path('unread-count/', UnreadCountView.as_view(), name='unread_count'),
]