# Generated by Django 4.1.5 on 2023-04-18 17:18

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("github", "0011_cachedresponse_modified_at_githubcommit_modified_at_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="githubrepository",
            old_name="api_visible",
            new_name="is_published",
        ),
        migrations.AlterField(
            model_name="githubrepository",
            name="is_published",
            field=models.BooleanField(default=True, help_text="Publicly visible"),
        ),
        migrations.AddField(
            model_name="githubrepository",
            name="published_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
