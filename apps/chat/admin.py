from django.contrib import admin
from .models import Chat, ScheduledMessage, Message


# Register your models here.

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id','owner','user']

@admin.register(ScheduledMessage)
class ScheduledMessageAdmin(admin.ModelAdmin):
    list_display = ['id','chat','sender']

@admin.register(Message)
class ScheduledMessageAdmin(admin.ModelAdmin):
    list_display = ['id','chat','sender']