# Generated by Django 5.0.4 on 2024-04-24 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0057_alter_relatedfile_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="relatedfile",
            name="type",
            field=models.CharField(
                choices=[
                    ("audio", "Audio"),
                    ("video", "Video"),
                    ("image", "Image"),
                    ("text", "Text"),
                    ("unknown", "Unknown"),
                ],
                default="unknown",
                max_length=10,
            ),
        ),
    ]
