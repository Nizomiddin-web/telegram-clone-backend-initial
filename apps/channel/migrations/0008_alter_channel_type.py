# Generated by Django 4.2.16 on 2025-01-23 17:07

import channel.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0007_alter_channelmembership_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='type',
            field=models.CharField(choices=[('public', 'PUBLIC'), ('private', 'PRIVATE')], default=channel.models.ChannelType['PUBLIC'], max_length=30),
        ),
    ]
