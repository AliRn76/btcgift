# Generated by Django 4.1.4 on 2023-01-27 21:24

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
                ('is_answer', models.BooleanField(db_column='IsAnswer', default=True)),
                ('message', models.CharField(db_column='Message', max_length=1023)),
                ('file', models.FileField(blank=True, db_column='File', null=True, upload_to=support.models.SupportMessages.support_files_path)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_column='DateCreated')),
                ('support_id', models.ForeignKey(db_column='SupportID', on_delete=django.db.models.deletion.CASCADE, to='support.support')),
            ],
            options={
                'db_table': 'SupportMessage',
            },
        ),
    ]
