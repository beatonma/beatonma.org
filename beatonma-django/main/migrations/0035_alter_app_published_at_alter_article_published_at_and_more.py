# Generated by Django 4.1.5 on 2023-04-08 14:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0034_alter_changelog_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="app",
            name="published_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="article",
            name="published_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="blog",
            name="published_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="changelog",
            name="published_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
