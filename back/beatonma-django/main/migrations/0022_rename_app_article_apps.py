# Generated by Django 4.0.4 on 2022-05-12 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_rename_hero_banner_article_hero_banner_css'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='app',
            new_name='apps',
        ),
    ]
