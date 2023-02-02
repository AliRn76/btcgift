# Generated by Django 4.1.4 on 2023-01-27 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(db_column='ID', primary_key=True, serialize=False)),
                ('question', models.CharField(db_column='Question', max_length=255)),
                ('answer', models.TextField(db_column='Answer')),
                ('is_active', models.BooleanField(db_column='IsActive', default=True)),
                ('order', models.PositiveIntegerField(db_column='Order')),
                ('date_updated', models.DateTimeField(auto_now=True, db_column='DateUpdated')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_column='DateCreated')),
            ],
            options={
                'db_table': 'FAQ',
            },
        ),
    ]