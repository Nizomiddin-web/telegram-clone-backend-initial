# Generated by Django 4.2.16 on 2025-01-25 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0012_alter_channelmembership_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channel',
            name='type',
        ),
        migrations.AddField(
            model_name='channel',
            name='channel_type',
            field=models.CharField(choices=[('public', 'PUBLIC'), ('private', 'PRIVATE')], default='public', max_length=30),
        ),
    ]
