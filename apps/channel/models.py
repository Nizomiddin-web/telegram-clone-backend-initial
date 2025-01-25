import uuid
from enum import Enum

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
# Create your models here.
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return [(choice.value, choice.name) for choice in cls]

    @classmethod
    def values(cls):
        return [choice.value for choice in cls]


class ChannelType(BaseEnum):
    PUBLIC = "public"
    PRIVATE = "private"


class ChannelMembershipType(BaseEnum):
    ADMIN = "admin"
    MEMBER = "member"



class Channel(BaseModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200,null=True,blank=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    channel_type = models.CharField(max_length=30,choices=ChannelType.choices(),default=ChannelType.PUBLIC.value)

    class Meta:
        db_table = 'channel'
        verbose_name='Channel'
        verbose_name_plural='Channels'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class ChannelMembership(BaseModel):
    channel = models.ForeignKey(Channel,on_delete=models.CASCADE,related_name='memberships')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='memberships')
    role = models.CharField(max_length=200,choices=ChannelMembershipType.choices(),default=ChannelMembershipType.MEMBER.value)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','channel')
        db_table = 'channel_membership'
        verbose_name='Channel Membership'
        verbose_name_plural='Channels Membership'
        ordering = ['-created_at']

class ChannelMessage(BaseModel):
    channel = models.ForeignKey(Channel,on_delete=models.CASCADE)
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to="channel/messages/images/",null=True,blank=True)
    file = models.FileField(upload_to="channel/messages/files/",null=True,blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,related_name="likes_channel")


    class Meta:
        db_table = 'channel_message'
        verbose_name='Channel Message'
        verbose_name_plural='Channels Messages'
        ordering = ['-created_at']

    @property
    def media(self):
        return self.image or self.file

    @property
    def name(self):
        if self.media:
            return self.media.name
        return None

    def __str__(self):
        return f"Message from {self.sender.username} in {self.channel.name}"

class ChannelScheduledMessage(BaseModel):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="channel/messages/images/", null=True, blank=True)
    file = models.FileField(upload_to="channel/messages/files/", null=True, blank=True)
    scheduled_time = models.DateTimeField()
    sent = models.BooleanField(default=False)

    class Meta:
        db_table = 'channel_scheduled_message'
        ordering = ['-created_at']
