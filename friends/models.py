from django.db import models
from auth_system.models import User

class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following_relations',
        verbose_name='Підписник'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers_relations',
        verbose_name='На кого підписані'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.follower} → {self.following}'

class FollowRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Очікує'),
        ('accepted', 'Прийнято'),
        ('rejected', 'Відхилено'),
    )

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_follow_requests'
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_follow_requests'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f'{self.from_user} → {self.to_user} ({self.status})'