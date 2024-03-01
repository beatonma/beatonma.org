# Generated by Django 4.2.5 on 2024-03-01 14:05

from django.db import migrations
import main.forms.filename
import main.forms.sanitized_filefield


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0054_alter_relatedfile_file_storage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='hero_image',
            field=main.forms.sanitized_filefield.SanitizedFileField(blank=True, help_text='Image shown at the top of the article', quality=75, size=[2560, 2560], upload_to=main.forms.filename.RandomFilename('article/%Y/', filename_attrs=[], filename_literals=['hero'])),
        ),
        migrations.AlterField(
            model_name='relatedfile',
            name='file',
            field=main.forms.sanitized_filefield.SanitizedFileField(blank=True, quality=75, size=[2560, 2560], upload_to=main.forms.filename.RandomFilename('related/%Y/', filename_attrs=['description'], filename_literals=[])),
        ),
    ]
