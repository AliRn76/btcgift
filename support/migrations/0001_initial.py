# Generated by Django 4.1.4 on 2022-12-30 16:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import support.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.BigAutoField(db_column='ID', primary_key=True, serialize=False)),
                ('subject', models.CharField(db_column='Subject', max_length=63)),
                ('issue', models.CharField(db_column='Issue', max_length=1024)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_column='DateCreated')),
                ('user_id', models.ForeignKey(db_column='UserID', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Support',
            },
        ),
        migrations.CreateModel(
            name='SupportMessages',
            fields=[
                ('id', models.BigAutoField(db_column='ID', primary_key=True, serialize=False)),
                ('is_answer', models.BooleanField(db_column='IsAnswer')),
                ('message', models.CharField(blank=True, db_column='Message', max_length=1024, null=True)),
                ('file', models.FileField(blank=True, db_column='File', null=True, upload_to=support.models.SupportMessages.support_files_path)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_column='DateCreated')),
                ('admin_id', models.ForeignKey(db_column='AdminID', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('support_id', models.ForeignKey(db_column='SupportID', on_delete=django.db.models.deletion.CASCADE, to='support.support')),
            ],
            options={
                'db_table': 'SupportMessage',
            },
        ),
    ]
