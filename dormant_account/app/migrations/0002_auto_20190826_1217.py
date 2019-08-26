# Generated by Django 2.2.4 on 2019-08-26 03:17

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
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 26, 3, 17, 57, 269347, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='content',
            name='last_edit',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 26, 3, 17, 57, 318211, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='dormantuserinfo',
            name='delete_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 8, 26, 3, 17, 57, 320206, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='dormantuserinfo',
            name='dormant_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 26, 3, 17, 57, 320206, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='dormantuserinfo',
            name='last_login',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 8, 26, 3, 17, 57, 320206, tzinfo=utc)),
        ),
    ]