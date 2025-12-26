from django.db import models
from auth_system.models import User

# Create your models here.
class Group(models.Model):
    PRIVACY = (
        ('public', 'Публічна'),
        ('private', 'Приватна'),
    )
    name = models.CharField(max_length=100, verbose_name='Назва')
    description = models.TextField(blank=True, verbose_name='Опис')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Власник', related_name='created_groups')
    privacy = models.CharField(max_length=10, choices=PRIVACY, default='public', verbose_name='Приватність')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    is_active = models.BooleanField(default=True, verbose_name='Активний')


class GroupMember(models.Model):
    ROLE = (
        ('member', 'Учасник'),
        ('moderator', 'Модератор'),
        ('admin', 'Адміністратор'),
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Група', related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Користувач', related_name='group_memberships')
    role = models.CharField(max_length=10, choices=ROLE, default='member', verbose_name='Роль')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    is_active = models.BooleanField(default=True, verbose_name='Активний')

    class Meta:
        unique_together = ('group', 'user')
