# Generated by Django 2.2.4 on 2019-08-14 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20190814_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='dormant_cnt',
            field=models.IntegerField(default=0, verbose_name='d_cnt'),
        ),
    ]