from .models import Message

def unread_total(request):
    if request.user.is_authenticated:
        return {
            "unread_total": Message.objects.filter(
                is_read=False
            ).exclude(sender=request.user).count()
        }
    return {}