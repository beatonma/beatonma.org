# Generated by Django 3.2.4 on 2022-02-10 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pageview',
            name='ip',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
