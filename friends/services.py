from django.db import transaction
from django.core.exceptions import PermissionDenied
from auth_system.models import User
from .models import Follow, FollowRequest


@transaction.atomic
def follow_user(follower: User, target: User) -> str:
    if follower == target:
        return 'self'

    if Follow.objects.filter(follower=follower, following=target).exists():
        return 'already_following'

    if target.profile.is_private:
        req, created = FollowRequest.objects.get_or_create(
            from_user=follower,
            to_user=target,
            defaults={'status': 'pending'}
        )
        return 'request_sent' if created else 'request_exists'

    Follow.objects.create(follower=follower, following=target)
    return 'followed'


@transaction.atomic
def unfollow_user(follower: User, target: User) -> str:
    deleted, _ = Follow.objects.filter(
        follower=follower,
        following=target
    ).delete()

    return 'unfollowed' if deleted else 'not_following'


@transaction.atomic
def accept_follow_request(request_id: int, user: User) -> None:
    req = FollowRequest.objects.select_for_update().get(id=request_id)

    if req.to_user != user:
        raise PermissionDenied('Not your follow request')

    if req.status != 'pending':
        return

    Follow.objects.create(
        follower=req.from_user,
        following=req.to_user
    )

    req.status = 'accepted'
    req.save()


@transaction.atomic
def reject_follow_request(request_id: int, user: User) -> None:
    req = FollowRequest.objects.select_for_update().get(id=request_id)

    if req.to_user != user:
        raise PermissionDenied('Not your follow request')

    if req.status != 'pending':
        return

    req.status = 'rejected'
    req.save()


def can_view_profile(viewer: User, owner: User) -> bool:
    if owner.profile.is_private is False:
        return True

    if viewer == owner:
        return True

    return Follow.objects.filter(
        follower=viewer,
        following=owner
    ).exists()

def is_following(follower: User, target: User) -> bool:
    return Follow.objects.filter(
        follower=follower,
        following=target
    ).exists()


def follow_request_sent(follower: User, target: User) -> bool:
    return FollowRequest.objects.filter(
        from_user=follower,
        to_user=target,
        status='pending'
    ).exists()