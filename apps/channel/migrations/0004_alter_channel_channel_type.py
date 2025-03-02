# Generated by Django 4.2.16 on 2025-01-23 07:25

import channel.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0003_alter_channel_channel_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='channel_type',
            field=models.CharField(choices=[('public', 'PUBLIC'), ('private', 'PRIVATE')], default=channel.models.ChannelType['PUBLIC'], max_length=30),
        ),
    ]
