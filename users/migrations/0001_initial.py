# Generated by Django 2.1.5 on 2019-01-19 17:58

import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('last_active', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('first_name', models.CharField(blank=True, max_length=64, null=True)),
                ('last_name', models.CharField(blank=True, max_length=64, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'permissions': (('can_add_dsr_admin', 'Can add DSR Admin'), ('can_delete_dsr_admin', 'Can delete DSR Admin'), ('can_update_dsr_admin', 'Can update DSR Admin'), ('can_add_dsr_employee', 'Can add DSR Employee'), ('can_delete_dsr_employee', 'Can delete DSR Employee'), ('can_update_dsr_employee', 'Can update DSR Employee'), ('can_add_dsr_customer_super_admin', 'Can add DSR Customer Super Admin'), ('.can_delete_dsr_customer_super_admin', 'Can delete DSR Customer Super Admin'), ('can_update_dsr_customer_super_admin', 'Can update DSR Customer Super Admin'), ('can_add_dsr_customer_admin', 'Can add DSR Customer Admin'), ('can_delete_dsr_customer_admin', 'Can delete DSR Customer Admin'), ('can_update_dsr_customer_admin', 'Can update DSR Customer Admin'), ('can_add_dsr_customer_user', 'Can add DSR Customer User'), ('can_delete_dsr_customer_user', 'Can delete DSR Customer User'), ('can_update_dsr_customer_user', 'Can update DSR Customer User')),
            },
        ),
    ]
