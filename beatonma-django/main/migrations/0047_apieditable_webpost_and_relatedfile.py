# Generated by Django 4.2.5 on 2023-11-28 13:41

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0046_alter_link_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="api_id",
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.AddField(
            model_name="blog",
            name="api_id",
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.AddField(
            model_name="changelog",
            name="api_id",
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.AddField(
            model_name="note",
            name="api_id",
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.AddField(
            model_name="relatedfile",
            name="api_id",
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
    ]
