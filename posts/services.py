from django.db import transaction, IntegrityError
from django.db.models import F

from .models import Post, Like, Comment

@transaction.atomic
def toggle_like(user, post):
    like, created = Like.objects.get_or_create(
        user=user,
        post=post
    )

    if not created:
        like.delete()
        action = 'unliked'
    else:
        action = 'liked'

    return action

@transaction.atomic
def create_comment(user, post, text):
    Comment.objects.create(author=user, post=post, text=text)
    post.comments_count += 1
    post.save(updated_fields=['comments_count'])