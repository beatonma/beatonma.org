# Generated by Django 4.2.5 on 2024-02-29 13:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0051_alter_note_content"),
    ]

    operations = [
        migrations.AddField(
            model_name="webapp",
            name="inherit_site_theme",
            field=models.BooleanField(default=False),
        ),
    ]
