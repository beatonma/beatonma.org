# Generated by Django 4.1.1 on 2023-01-13 11:40

from django.db import migrations, models
import mentions.models.mixins.mentionable


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0027_alter_app_icon"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="app",
            name="allow_incoming_webmentions",
        ),
        migrations.RemoveField(
            model_name="article",
            name="allow_incoming_webmentions",
        ),
        migrations.RemoveField(
            model_name="blog",
            name="allow_incoming_webmentions",
        ),
        migrations.RemoveField(
            model_name="changelog",
            name="allow_incoming_webmentions",
        ),
        migrations.RemoveField(
            model_name="note",
            name="allow_incoming_webmentions",
        ),
        migrations.AlterField(
            model_name="app",
            name="allow_outgoing_webmentions",
            field=models.BooleanField(
                default=mentions.models.mixins.mentionable._outgoing_default,
                verbose_name="allow outgoing webmentions",
            ),
        ),
        migrations.AlterField(
            model_name="article",
            name="allow_outgoing_webmentions",
            field=models.BooleanField(
                default=mentions.models.mixins.mentionable._outgoing_default,
                verbose_name="allow outgoing webmentions",
            ),
        ),
        migrations.AlterField(
            model_name="blog",
            name="allow_outgoing_webmentions",
            field=models.BooleanField(
                default=mentions.models.mixins.mentionable._outgoing_default,
                verbose_name="allow outgoing webmentions",
            ),
        ),
        migrations.AlterField(
            model_name="changelog",
            name="allow_outgoing_webmentions",
            field=models.BooleanField(
                default=mentions.models.mixins.mentionable._outgoing_default,
                verbose_name="allow outgoing webmentions",
            ),
        ),
        migrations.AlterField(
            model_name="note",
            name="allow_outgoing_webmentions",
            field=models.BooleanField(
                default=mentions.models.mixins.mentionable._outgoing_default,
                verbose_name="allow outgoing webmentions",
            ),
        ),
    ]
