# Generated by Django 4.2.16 on 2025-01-15 12:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_message_options_alter_scheduledmessage_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledmessage',
            name='text',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]