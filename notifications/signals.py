from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Notification

from posts.models import Like, Comment
from friends.models import Follow
from chat.models import Message

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if not created:
        return

    post = instance.post
    from_user = instance.user
    to_user = post.author

    if from_user == to_user:
        return

    Notification.objects.create(
        user=to_user,
        type='like',
        data={
            "from_user_id": from_user.id,
            "from_user_username": from_user.username,
            "post_id": post.id,
        }
    )

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if not created:
        return

    post = instance.post
    from_user = instance.author
    to_user = post.author

    if from_user == to_user:
        return

    Notification.objects.create(
        user=to_user,
        type='comment',
        data={
            "from_user_id": from_user.id,
            "from_user_username": from_user.username,
            "post_id": post.id,
            "comment_id": instance.id,
        }
    )

@receiver(post_save, sender=Follow)
def create_follow_notification(sender, instance, created, **kwargs):
    if not created:
        return

    from_user = instance.follower
    to_user = instance.following

    if from_user == to_user:
        return

    Notification.objects.create(
        user=to_user,
        type='follow',
        data={
            "from_user_id": from_user.id,
            "from_user_username": from_user.username,
        }
    )

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if not created:
        return

    from_user = instance.sender
    to_user = instance.receiver

    if from_user == to_user:
        return

    Notification.objects.create(
        user=to_user,
        type='message',
        data={
            "from_user_id": from_user.id,
            "from_user_username": from_user.username,
            "message_id": instance.id,
            "chat_id": instance.chat.id if hasattr(instance, 'chat') else None,
        }
    )