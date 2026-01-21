from django import template
from friends.models import Follow

register = template.Library()

@register.filter
def is_following(user, viewer):
    return Follow.objects.filter(
        follower=viewer,
        following=user
    ).exists()