# Generated by Django 2.2 on 2019-12-17 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nash-message', '0004_auto_20191217_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='nash_message',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='nash-message.Nash_message'),
        ),
    ]
