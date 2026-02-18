from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from .models import Notification

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return self.request.user.notifications.all()

class MarkAsReadView(LoginRequiredMixin, View):

    def post(self, request, pk):
        notification = get_object_or_404(
            Notification,
            pk=pk,
            user=request.user
        )
        notification.is_read = True
        notification.save()

        return redirect('notifications:list')

class MarkAllAsReadView(LoginRequiredMixin, View):

    def post(self, request):
        request.user.notifications.filter(is_read=False).update(is_read=True)
        return redirect('notifications:list')

class UnreadCountView(LoginRequiredMixin, View):

    def get(self, request):
        count = request.user.notifications.filter(is_read=False).count()
        return JsonResponse({'count': count})
