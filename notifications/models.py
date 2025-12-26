from django.db import models
from auth_system.models import User

# Create your models here.
class Notification(models.Model):
    TYPE = (
        ('message', 'Нове повідомлення'),
        ('like', 'Новий лайк'),
        ('comment', 'Новий коментар'),
        ('follow', 'Новий підпис'),
        ('group_invite', 'Запрошення до групи'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name='Користувач')
    type = models.CharField(max_length=20, choices=TYPE, verbose_name='Тип')
    data = models.JSONField(verbose_name='Дані')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')


