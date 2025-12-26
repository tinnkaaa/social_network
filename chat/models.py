from django.db import models
from auth_system.models import User

# Create your models here.
class ChatParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_participations', verbose_name='Користувач')
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='chat_participants', verbose_name='Чат')
    is_admin = models.BooleanField(default=False, verbose_name='Адміністратор')

class Chat(models.Model):
    is_group = models.BooleanField(default=False, verbose_name='Груповий чат')
    title = models.CharField(max_length=100, blank=True, verbose_name='Назва')
    participants = models.ManyToManyField(User, through='ChatParticipant', related_name='chats', verbose_name='Учасники')

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages', verbose_name='Чат')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Відправник')
    content = models.TextField(verbose_name='Текст повідомлення')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
