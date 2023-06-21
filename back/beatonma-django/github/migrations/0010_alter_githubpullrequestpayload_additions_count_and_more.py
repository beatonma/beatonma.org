# Generated by Django 4.0.4 on 2022-05-27 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0009_cachedresponse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githubpullrequestpayload',
            name='additions_count',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='githubpullrequestpayload',
            name='changed_files_count',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='githubpullrequestpayload',
            name='deletions_count',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='githubrepository',
            name='size_kb',
            field=models.PositiveIntegerField(editable=False),
        ),
    ]
