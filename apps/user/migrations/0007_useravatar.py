# Generated by Django 4.2.16 on 2024-12-29 07:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_user_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAvatar',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('avatar', models.ImageField(upload_to='avatars/', verbose_name='Profile Photos')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avatars', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Avatar',
                'verbose_name_plural': 'Users Avatar',
                'db_table': 'user_avatar',
                'ordering': ['-created_at'],
            },
        ),
    ]
