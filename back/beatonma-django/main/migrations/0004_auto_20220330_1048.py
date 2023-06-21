# Generated by Django 3.2.4 on 2022-03-30 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20220330_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='article',
            name='content_html',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='blog',
            name='content_html',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='content',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='content_html',
            field=models.TextField(blank=True, default=''),
        ),
    ]
