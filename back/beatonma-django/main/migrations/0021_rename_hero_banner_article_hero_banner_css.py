# Generated by Django 4.0.4 on 2022-05-06 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_article_hero_banner_alter_article_hero_css_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='hero_banner',
            new_name='hero_banner_css',
        ),
    ]
