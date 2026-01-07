from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Користувач'),
        ('moderator', 'Модератор'),
        ('admin', 'Адміністратор'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name='Роль'
    )
    email = models.EmailField(unique=True, verbose_name='Електронна пошта')
    is_email_verified = models.BooleanField(default=False)
    last_activity = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def can_edit_profile(self, profile):
        return self == profile.user or self.is_superuser

    def can_moderate(self):
        return self.role in ('moderator', 'admin') or self.is_superuser

class Profile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Чоловік'),
        ('female', 'Жінка'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)

    phone_number = models.CharField(max_length=20, blank=True, null=True)

    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Профіль {self.user.username}'

    class Meta:
        verbose_name = 'Профіль'
        verbose_name_plural = 'Профілі'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
        ]

    def followers(self):
        return self.user.followers_set.all()

    def following(self):
        return self.user.following_set.all()