# Generated by Django 4.2.16 on 2025-01-14 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sent_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
