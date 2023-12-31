# Generated by Django 3.2.4 on 2022-04-01 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20220330_1310'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='featured',
            new_name='is_featured',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='published',
            new_name='is_published',
        ),
        migrations.RenameField(
            model_name='blog',
            old_name='featured',
            new_name='is_featured',
        ),
        migrations.RenameField(
            model_name='blog',
            old_name='published',
            new_name='is_published',
        ),
        migrations.RenameField(
            model_name='changelog',
            old_name='featured',
            new_name='is_featured',
        ),
        migrations.RenameField(
            model_name='changelog',
            old_name='published',
            new_name='is_published',
        ),
        migrations.RenameField(
            model_name='note',
            old_name='featured',
            new_name='is_featured',
        ),
        migrations.RenameField(
            model_name='note',
            old_name='published',
            new_name='is_published',
        ),
        migrations.RemoveField(
            model_name='article',
            name='push_to_feed',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='push_to_feed',
        ),
        migrations.RemoveField(
            model_name='changelog',
            name='push_to_feed',
        ),
        migrations.RemoveField(
            model_name='note',
            name='push_to_feed',
        ),
        migrations.AddField(
            model_name='app',
            name='is_published',
            field=models.BooleanField(default=True, help_text='Publicly visible'),
        ),
    ]
