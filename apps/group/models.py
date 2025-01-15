import uuid

from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()
# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']
        abstract = True

class Group(BaseModel):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User,related_name="owner_groups",on_delete=models.SET_NULL,null=True)
    members = models.ManyToManyField(User,related_name="user_groups")
    is_private = models.BooleanField(default=False)

    class Meta:
        db_table = 'group'
        verbose_name='Group'
        verbose_name_plural='Groups'

class GroupParticipant(BaseModel):
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

class GroupMessage(BaseModel):
    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name="messages")
    sender = models.ForeignKey(User,on_delete=models.SET("delete_user"),related_name="send_messages")
    text = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to="group/messages/images/",null=True,blank=True)
    file = models.FileField(upload_to="group/messages/files/",null=True,blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    liked_by = models.ManyToManyField(User,related_name="liked_messages")

class GroupScheduledMessage(BaseModel):
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    scheduled_time = models.DateTimeField()
    sent = models.BooleanField(default=False)

class GroupPermission(BaseModel):
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    can_send_messages = models.BooleanField(default=True)
    can_send_media = models.BooleanField(default=False)
