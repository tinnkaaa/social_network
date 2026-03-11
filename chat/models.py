from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class ChatParticipant(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='chat_participations', verbose_name='Користувач')
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='chat_participants', verbose_name='Чат')
    is_admin = models.BooleanField(default=False, verbose_name='Адміністратор')

class Chat(models.Model):
    is_group = models.BooleanField(default=False, verbose_name='Груповий чат')
    title = models.CharField(max_length=100, blank=True, verbose_name='Назва')
    participants = models.ManyToManyField(get_user_model(), through='ChatParticipant', related_name='chats', verbose_name='Учасники')
    updated_at = models.DateTimeField(auto_now=True)

    def unread_count_for(self, user):
        return self.messages.filter(
            is_read=False
        ).exclude(sender=user).count()

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages', verbose_name='Чат')
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Відправник')
    text = models.TextField(verbose_name='Текст повідомлення')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.chat.save()
