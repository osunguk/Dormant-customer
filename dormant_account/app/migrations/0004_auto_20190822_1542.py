# Generated by Django 2.2.4 on 2019-08-22 06:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_profile_check'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='check',
            field=models.CharField(blank=True, max_length=100, verbose_name='check'),
        ),
        migrations.AlterField(
            model_name='content',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 22, 6, 42, 22, 785449, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='content',
            name='last_edit',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 22, 6, 42, 22, 816690, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='dormantuserinfo',
            name='deleteDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 8, 22, 6, 42, 22, 832312, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='dormantuserinfo',
            name='dormantDate',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 22, 6, 42, 22, 832312, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='dormantuserinfo',
            name='lastLogin',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 8, 22, 6, 42, 22, 832312, tzinfo=utc)),
        ),
    ]
