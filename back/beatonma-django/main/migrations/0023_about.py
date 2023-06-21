# Generated by Django 4.0.4 on 2022-05-18 13:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_rename_app_article_apps'),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('description', models.CharField(help_text='Only visible in admin', max_length=1024)),
                ('active', models.BooleanField(default=True)),
                ('format', models.PositiveSmallIntegerField(choices=[(0, 'None'), (1, 'Markdown')], default=1)),
                ('content', models.TextField(default='')),
                ('content_html', models.TextField(blank=True, default='', editable=False)),
            ],
            options={
                'verbose_name': 'About',
                'verbose_name_plural': 'About',
            },
        ),
    ]
