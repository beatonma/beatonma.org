# Generated by Django 3.2.4 on 2022-02-11 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_alter_webmailmessage_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='webmailmessage',
            options={'ordering': ['-timestamp']},
        ),
    ]
