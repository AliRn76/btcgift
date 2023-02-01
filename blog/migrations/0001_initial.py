# Generated by Django 4.1.4 on 2023-02-01 22:56

import blog.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(db_column='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(db_column='Title', max_length=31)),
                ('summary', models.CharField(db_column='Summary', max_length=63)),
                ('text', models.TextField(db_column='Text')),
                ('time_to_read', models.PositiveIntegerField(db_column='TimeToRead', default=0)),
                ('cover', models.ImageField(db_column='Cover', upload_to=blog.models.Blog.blog_covers_path)),
                ('like_count', models.PositiveIntegerField(db_column='LikeCount', default=0)),
                ('view_count', models.PositiveIntegerField(db_column='ViewCount', default=0)),
                ('comment_count', models.PositiveIntegerField(db_column='CommentCount', default=0)),
                ('date_updated', models.DateTimeField(auto_now=True, db_column='DateUpdated')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_column='DateCreated')),
            ],
            options={
                'db_table': 'Blog',
            },
        ),
        migrations.CreateModel(
            name='BlogView',
            fields=[
                ('id', models.BigAutoField(db_column='ID', primary_key=True, serialize=False)),
                ('ip', models.GenericIPAddressField(db_column='IP')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_column='DateCreated')),
                ('blog_id', models.ForeignKey(db_column='BlogID', on_delete=django.db.models.deletion.CASCADE, to='blog.blog')),
            ],
            options={
                'db_table': 'BlogView',
            },
        ),
        migrations.CreateModel(
            name='BlogLike',
            fields=[
                ('id', models.BigAutoField(db_column='ID', primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_column='DateCreated')),
                ('blog_id', models.ForeignKey(db_column='BlogID', on_delete=django.db.models.deletion.CASCADE, to='blog.blog')),
                ('user_id', models.ForeignKey(db_column='UserID', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'BlogLike',
            },
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.BigAutoField(db_column='ID', primary_key=True, serialize=False)),
                ('is_approved', models.BooleanField(db_column='IsApproved', default=False)),
                ('text', models.TextField(db_column='Text', max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_column='DateCreated')),
                ('blog_id', models.ForeignKey(db_column='BlogID', on_delete=django.db.models.deletion.CASCADE, to='blog.blog')),
                ('user_id', models.ForeignKey(db_column='UserID', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'BlogComment',
            },
        ),
    ]
