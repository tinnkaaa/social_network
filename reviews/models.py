from django.db import models
from auth_system.models import User

# Create your models here.
class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    target_type = models.CharField(max_length=50, verbose_name='Тип цілі')
    target_id = models.PositiveIntegerField(verbose_name='ID цілі')
    rating = models.PositiveIntegerField(verbose_name='Рейтинг')
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')