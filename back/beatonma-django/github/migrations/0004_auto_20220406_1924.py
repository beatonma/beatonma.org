# Generated by Django 3.2.4 on 2022-04-06 19:24

import common.models.api
import django.utils.timezone
import taggit.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("taggit", "0003_taggeditem_add_unique_index"),
        ("github", "0003_auto_20220112_1606"),
    ]

    operations = [
        migrations.CreateModel(
            name="GithubETag",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "url",
                    models.URLField(
                        editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("etag", models.CharField(editable=False, max_length=256, unique=True)),
                ("timestamp", models.DateTimeField(editable=False)),
            ],
            options={
                "ordering": ["timestamp"],
            },
        ),
        migrations.CreateModel(
            name="GithubEventUpdateCycle",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(common.models.api.ApiModel, models.Model),
        ),
        migrations.CreateModel(
            name="GithubLanguage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="e.g. Java, Python, CSS...",
                        max_length=50,
                        unique=True,
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="GithubLicense",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("key", models.CharField(editable=False, max_length=64, unique=True)),
                ("name", models.CharField(editable=False, max_length=64)),
                ("url", models.URLField(editable=False)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="GithubPollingEvent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("url", models.URLField()),
                ("interval", models.PositiveSmallIntegerField()),
            ],
            options={
                "verbose_name_plural": "GithubEvents: Polling event",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="GithubRepository",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "id",
                    models.PositiveIntegerField(
                        editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("url", models.URLField(editable=False)),
                ("updated_at", models.DateTimeField(editable=False)),
                ("api_visible", models.BooleanField(default=True)),
                ("name", models.CharField(editable=False, max_length=256)),
                ("full_name", models.CharField(editable=False, max_length=256)),
                ("description", models.TextField(editable=False, null=True)),
                ("is_private", models.BooleanField(editable=False)),
                ("size_kb", models.PositiveSmallIntegerField(editable=False)),
                (
                    "license",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="repositories",
                        to="github.githublicense",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Github Repositoriies",
                "ordering": ["-updated_at"],
            },
            bases=(common.models.api.ApiModel, models.Model),
        ),
        migrations.CreateModel(
            name="GithubUser",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "id",
                    models.PositiveIntegerField(
                        editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("username", models.CharField(editable=False, max_length=64)),
                ("url", models.URLField(editable=False)),
                ("avatar_url", models.URLField(editable=False)),
            ],
            options={
                "ordering": ["username"],
            },
        ),
        migrations.CreateModel(
            name="GithubUserEvent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("github_id", models.CharField(max_length=128)),
                ("type", models.CharField(max_length=128)),
                ("is_public", models.BooleanField()),
                (
                    "repository",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="github.githubrepository",
                    ),
                ),
                (
                    "update_cycle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to="github.githubeventupdatecycle",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="github.githubuser",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(common.models.api.ApiModel, models.Model),
        ),
        migrations.CreateModel(
            name="GithubWikiPayload",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("name", models.CharField(editable=False, max_length=256)),
                ("url", models.URLField(editable=False)),
                ("action", models.CharField(editable=False, max_length=64)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wiki_changes",
                        to="github.githubuserevent",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "GithubEvents: Wiki edit",
            },
            bases=(common.models.api.ApiModel, models.Model),
        ),
        migrations.AddField(
            model_name="githubrepository",
            name="owner",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="repositories",
                to="github.githubuser",
            ),
        ),
        migrations.AddField(
            model_name="githubrepository",
            name="primary_language",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="github.githublanguage",
            ),
        ),
        migrations.AddField(
            model_name="githubrepository",
            name="tags",
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="taggit.TaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.CreateModel(
            name="GithubReleasePayload",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("name", models.CharField(editable=False, max_length=256)),
                ("url", models.URLField(editable=False)),
                ("description", models.TextField(editable=False)),
                ("published_at", models.DateTimeField(editable=False)),
                (
                    "event",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="release_data",
                        to="github.githubuserevent",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "GithubEvents: Release",
            },
            bases=(common.models.api.ApiModel, models.Model),
        ),
        migrations.CreateModel(
            name="GithubPullRequestPayload",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("url", models.URLField(editable=False)),
                ("number", models.PositiveSmallIntegerField(editable=False)),
                ("merged_at", models.DateTimeField(editable=False)),
                ("additions_count", models.PositiveSmallIntegerField(editable=False)),
                ("deletions_count", models.PositiveSmallIntegerField(editable=False)),
                (
                    "changed_files_count",
                    models.PositiveSmallIntegerField(editable=False),
                ),
                (
                    "event",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pull_merged_data",
                        to="github.githubuserevent",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "GithubEvents: Close pull request",
            },
            bases=(common.models.api.ApiModel, models.Model),
        ),
        migrations.CreateModel(
            name="GithubLanguageUsage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("size_bytes", models.PositiveIntegerField()),
                (
                    "language",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="github.githublanguage",
                    ),
                ),
                (
                    "repository",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="languages",
                        to="github.githubrepository",
                    ),
                ),
            ],
            bases=(common.models.api.ApiModel, models.Model),
        ),
        migrations.CreateModel(
            name="GithubIssuesPayload",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("number", models.PositiveSmallIntegerField(editable=False)),
                ("url", models.URLField(editable=False)),
                ("closed_at", models.DateTimeField(editable=False)),
                (
                    "event",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="issue_closed_data",
                        to="github.githubuserevent",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "GithubEvents: Issue",
            },
            bases=(common.models.api.ApiModel, models.Model),
        ),
        migrations.CreateModel(
            name="GithubCreatePayload",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("ref", models.CharField(editable=False, max_length=128, null=True)),
                ("ref_type", models.CharField(editable=False, max_length=128)),
                (
                    "event",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="create_event_data",
                        to="github.githubuserevent",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "GithubEvents: Create",
            },
            bases=(common.models.api.ApiModel, models.Model),
        ),
        migrations.CreateModel(
            name="GithubCommit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("sha", models.CharField(editable=False, max_length=256)),
                ("message", models.TextField(editable=False)),
                ("url", models.URLField(editable=False)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="commits",
                        to="github.githubuserevent",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "GithubEvents: Commit",
            },
            bases=(common.models.api.ApiModel, models.Model),
        ),
        migrations.AddConstraint(
            model_name="githublanguageusage",
            constraint=models.UniqueConstraint(
                fields=("repository", "language"), name="unique_language_per_repository"
            ),
        ),
    ]
