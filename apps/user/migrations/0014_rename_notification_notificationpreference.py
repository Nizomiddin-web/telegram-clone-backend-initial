# Generated by Django 4.2.16 on 2025-01-09 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_notification'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Notification',
            new_name='NotificationPreference',
        ),
    ]