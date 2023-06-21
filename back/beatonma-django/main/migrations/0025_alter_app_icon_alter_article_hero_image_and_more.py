# Generated by Django 4.0.4 on 2022-05-19 17:21

from django.db import migrations
import main.forms.filename
import main.forms.sanitized_filefield


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_relatedfile_original_filename_alter_app_icon_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='icon',
            field=main.forms.sanitized_filefield.SanitizedFileField(blank=True, quality=75, size=[800, 800], upload_to=main.forms.filename.RandomFilename('icon/app/', filename_attrs=[], filename_literals=[])),
        ),
        migrations.AlterField(
            model_name='article',
            name='hero_image',
            field=main.forms.sanitized_filefield.SanitizedFileField(blank=True, help_text='Image shown at the top of the article', quality=75, size=[2560, 1440], upload_to=main.forms.filename.RandomFilename('article/%Y/', filename_attrs=[], filename_literals=['hero'])),
        ),
        migrations.AlterField(
            model_name='article',
            name='preview_image',
            field=main.forms.sanitized_filefield.SanitizedFileField(blank=True, help_text='Image shown beside links to this article', quality=75, size=[800, 800], upload_to=main.forms.filename.RandomFilename('article/%Y/', filename_attrs=[], filename_literals=['preview'])),
        ),
        migrations.AlterField(
            model_name='relatedfile',
            name='file',
            field=main.forms.sanitized_filefield.SanitizedFileField(blank=True, quality=75, size=[2560, 1440], upload_to=main.forms.filename.RandomFilename('related/%Y/', filename_attrs=['description'], filename_literals=[])),
        ),
    ]
