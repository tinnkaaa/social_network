from django.db import models
from auth_system.models import User

# Create your models here.
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='підписник', related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='підписаний', related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    is_active = models.BooleanField(default=True, verbose_name='Активний')

    class Meta:
        verbose_name = 'Підписка'
        verbose_name_plural = 'Підписки'
        ordering = ['-created_at']
        unique_together = ['follower', 'following']

    def __str__(self):
        return f'{self.follower.username} підписаний на {self.following.username}'

class FriendRequest(models.Model):
    STATUS = (
        ('pending', 'В очікуванні'),
        ('accepted', 'Прийнято'),
        ('rejected', 'Відхилено'),
    )
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Відправник', related_name='sent_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Отримувач', related_name='received_requests')
    status = models.CharField(max_length=10, choices=STATUS, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')

    class Meta:
        verbose_name = 'Запит на дружбу'
        verbose_name_plural = 'Запити на дружбу'

    def __str__(self):
        return f'{self.from_user.username} відправив запит на дружбу {self.to_user.username}'