# Generated by Django 4.2.16 on 2025-01-26 19:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('channel', '0017_rename_image_channelmessage_media'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channelmessage',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='likes_channel', to=settings.AUTH_USER_MODEL),
        ),
    ]
