# Generated by Django 2.2.4 on 2019-08-08 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20190808_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='writer',
            field=models.CharField(max_length=100, verbose_name='writer'),
        ),
    ]
