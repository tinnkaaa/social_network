from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Користувач'),
        ('moderator', 'Модератор'),
        ('admin', 'Адміністратор'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name='Роль')
    email = models.EmailField(unique=True, verbose_name='Електронна пошта')
    is_email_verified = models.BooleanField(default=False, verbose_name='Підтверджено електронну пошту')
    last_activity = models.DateTimeField(null=True, blank=True, verbose_name='Остання активність')

    REQUIRED_FIELDS = ['email']

    def is_moderator(self):
        return self.role in ('moderator', 'admin')
class Profile(models.Model):
    GENDER_CHOICES = (
        ('male', 'чоловік'),
        ('female', 'жінка'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiles')
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True, verbose_name='Аватар')
    bio = models.TextField(blank=True, null=True, verbose_name='Біографія')
    birth_date = models.DateField(blank=True, null=True, verbose_name="Дата народження")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, verbose_name='Стать')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    is_active = models.BooleanField(default=True, verbose_name='Активний')
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер телефону')
    followers_count = models.PositiveIntegerField(default=0, verbose_name='Кількість підписників')
    following_count = models.PositiveIntegerField(default=0, verbose_name='Кількість підписаних')

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = 'Профіль'
        verbose_name_plural = 'Профілі'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
        ]

