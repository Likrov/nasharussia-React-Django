# Generated by Django 2.2 on 2019-12-17 19:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nash-message', '0003_nash_message_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='nash_message',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Nash_messageLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('nash_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nash-message.Nash_message')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='nash_message',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='nash_message_user', through='nash-message.Nash_messageLike', to=settings.AUTH_USER_MODEL),
        ),
    ]
