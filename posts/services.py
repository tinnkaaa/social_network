from django.db import transaction
from .models import Post, Like, Comment

@transaction.atomic
def toggle_like(user, post):
    like = Like.objects.filter(user=user, post=post).first()
    if like:
        like.delete()
        post.likes_count = max(0, post.likes_count - 1)
        post.save(update_fields=['likes_count'])
        return 'unliked'

    Like.objects.create(user=user, post=post)
    post.likes_count = post.likes_count + 1
    post.save(update_fields=['likes_count'])
    return 'liked'

@transaction.atomic
def create_comment(user, post, text):
    Comment.objects.create(author=user, post=post, text=text)
    post.comments_count += 1
    post.save(updated_fields=['comments_count'])