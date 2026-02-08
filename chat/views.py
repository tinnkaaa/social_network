from django.db.models import Count, Q
from django.views.generic import DetailView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from .models import Chat, Message
from auth_system.models import User


class ChatRoomView(LoginRequiredMixin, DetailView):
    model = Chat
    pk_url_kwarg = 'chat_id'
    template_name = "chat/room.html"
    context_object_name = "chat"

    def get(self, request, *args, **kwargs):
        chat = get_object_or_404(Chat, id=self.kwargs['chat_id'])

        Message.objects.filter(
            chat=chat,
            is_read=False
        ).exclude(sender=request.user).update(is_read=True)

        return super().get(request, *args, **kwargs)

    def get_object(self):
        chat = super().get_object()
        chat.messages.filter(
            is_read=False
        ).exclude(sender=self.request.user).update(is_read=True)
        return chat

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["messages"] = self.object.messages.select_related("sender")
        return context

    def dispatch(self, request, *args, **kwargs):
        chat = self.get_object()
        if request.user not in chat.participants.all():
            return redirect("chat_list")
        return super().dispatch(request, *args, **kwargs)


class ChatStartView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        other_user = get_object_or_404(User, id=user_id)

        chat = (
            Chat.objects
            .filter(participants=request.user)
            .filter(participants=other_user)
            .first()
        )

        if not chat:
            chat = Chat.objects.create()
            chat.participants.add(request.user, other_user)

        return redirect("chat_room", chat_id=chat.id)


class ChatListView(LoginRequiredMixin, ListView):
    model = Chat
    template_name = "chat/chat_list.html"
    context_object_name = "chats"

    def get_queryset(self):
        qs = Chat.objects.filter(participants=self.request.user).prefetch_related(
            "participants", "messages"
        )

        for chat in qs:
            chat.unread = chat.unread_count_for(self.request.user)
            chat.last_message = chat.messages.order_by("-created_at").first()

        return qs