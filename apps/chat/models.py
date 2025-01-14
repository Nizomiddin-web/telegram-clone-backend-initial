import uuid

from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()
# Create your models here.

class Chat(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='owner_chats')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_chats')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'chat'
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'
        unique_together = ('owner','user')
        ordering = ['-created_at']


class ChatParticipant(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='chat_participants')
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE,related_name='chat_participants')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','chat')

class Message(models.Model):
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE,related_name='messages')
    sender = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='messages')
    text = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to="message/images/",null=True,blank=True)
    file = models.FileField(upload_to="message/files/",null=True,blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    liked_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ScheduledMessage(models.Model):
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE,related_name='scheduled_messages')
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='scheduled_messages')
    scheduled_time = models.DateTimeField()
    sent = models.BooleanField(default=False)
