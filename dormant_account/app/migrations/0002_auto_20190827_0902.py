# Generated by Django 2.2.4 on 2019-08-27 00:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 27, 0, 2, 2, 213396, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='content',
            name='last_edit',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 27, 0, 2, 2, 260259, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='dormantuserinfo',
            name='delete_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 8, 27, 0, 2, 2, 260259, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='dormantuserinfo',
            name='dormant_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 27, 0, 2, 2, 260259, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='dormantuserinfo',
            name='last_login',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 8, 27, 0, 2, 2, 260259, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='memo',
            field=models.TextField(blank=True, default='', max_length=1000, verbose_name='Memo'),
        ),
    ]