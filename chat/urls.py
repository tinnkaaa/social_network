from django.urls import path

from .views import ChatRoomView, ChatStartView, ChatListView


urlpatterns = [
    path("chat/<int:chat_id>/", ChatRoomView.as_view(), name="chat_room"),
    path("chat/start/<int:user_id>/", ChatStartView.as_view(), name="chat_start"),
    path("chat/", ChatListView.as_view(), name="chat_list"),
]