# Generated by Django 5.1.1 on 2024-09-17 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0059_app_extends_webpost"),
    ]

    operations = [
        migrations.AddField(
            model_name="app",
            name="format",
            field=models.PositiveSmallIntegerField(
                choices=[(0, "None"), (1, "Markdown")], default=1
            ),
        ),
    ]
