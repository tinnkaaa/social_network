from django.db import models
from auth_system.models import User

# Create your models here.
class Post(models.Model):
    POST_TYPES = (
        ('text', 'Текст'),
        ('image', 'Зображення'),
        ('video', 'Відео'),
        ('file', 'Файл'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=True, verbose_name='Текст')
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default='text', verbose_name='Тип публікації')
    likes_count = models.PositiveIntegerField(default=0, verbose_name='Кількість лайків')
    comments_count = models.PositiveIntegerField(default=0, verbose_name='Кількість коментарів')
    shares_count = models.PositiveIntegerField(default=0, verbose_name='Кількість публікацій')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    is_active = models.BooleanField(default=True, verbose_name='Активний')
    is_edited = models.BooleanField(default=False, verbose_name='Редагований')

    class Meta:
        verbose_name = 'Публікація'
        verbose_name_plural = 'Публікації'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author', 'created_at']),
        ]

class PostMedia(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media', verbose_name='Публікація')
    media_type = models.CharField(max_length=10, verbose_name='Тип медіа')
    file = models.FileField(upload_to='post_media/', verbose_name='Файл')

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Публікація')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    is_active = models.BooleanField(default=True, verbose_name='Активний')

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', verbose_name='Публікація')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', verbose_name='Користувач')

    class Meta:
        unique_together = ('post', 'user')