# Generated by Django 3.2.4 on 2022-04-11 10:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0003_alter_webmailmessage_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='webmailmessage',
            options={'ordering': ['-created_at']},
        ),
        migrations.RemoveField(
            model_name='webmailmessage',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='webmailmessage',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
