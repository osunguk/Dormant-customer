# Generated by Django 2.2.4 on 2019-08-22 01:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('number', models.IntegerField(primary_key=True, serialize=False, verbose_name='number')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('contents', models.CharField(max_length=300)),
                ('writer', models.CharField(max_length=100, verbose_name='writer')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_edit', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='DormantUserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=100, verbose_name='username')),
                ('role_dormant', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Business'), (2, 'Customer')], null=True)),
                ('lastLogin', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('email', models.EmailField(blank=True, max_length=100, verbose_name='이메일')),
                ('phoneNumber', models.CharField(blank=True, max_length=11, null=True, verbose_name='핸드폰 번호')),
                ('dormantDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleteDate', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('checkNotice', models.BooleanField(default=False)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='사업장 이름')),
                ('business_number', models.IntegerField(blank=True, null=True, verbose_name='사업자 번호')),
                ('star_point', models.IntegerField(blank=True, null=True, verbose_name='보유 별')),
                ('kakao_Id', models.CharField(blank=True, max_length=100, null=True, verbose_name='카카오톡 아이디')),
                ('mining_point', models.IntegerField(blank=True, null=True, verbose_name='보유 포인트')),
            ],
            options={
                'verbose_name_plural': '휴면 계정',
            },
        ),
        migrations.CreateModel(
            name='UserC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kakao_Id', models.CharField(max_length=100, verbose_name='카카오톡 아이디')),
                ('mining_point', models.IntegerField(default=0, verbose_name='보유 포인트')),
                ('user_c', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '커스텀 사용자',
            },
        ),
        migrations.CreateModel(
            name='UserB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100, verbose_name='사업장 이름')),
                ('business_number', models.IntegerField(verbose_name='사업자 번호')),
                ('star_point', models.IntegerField(default=0, verbose_name='보유 별')),
                ('user_b', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '비즈니스 사용자',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=100, verbose_name='이메일')),
                ('phoneNumber', models.CharField(blank=True, max_length=11, null=True, verbose_name='핸드폰 번호')),
                ('check', models.CharField(blank=True, max_length=100, verbose_name='check')),
                ('dormant_cnt', models.IntegerField(default=0, verbose_name='dormant_cnt')),
                ('memo', models.TextField(blank=True, max_length=300, verbose_name='memo')),
                ('check_alert', models.BooleanField(blank=True, default=False, verbose_name='check_alter')),
                ('role_profile', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Business'), (2, 'Customer')], null=True)),
                ('dormantNotice_day_filter', models.BooleanField(blank=True, default=False, verbose_name='dormantNotice_day_filter')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
