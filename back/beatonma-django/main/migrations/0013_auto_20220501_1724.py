# Generated by Django 3.2.4 on 2022-05-01 17:24

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20220428_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='apptype',
            name='accent_color',
            field=colorfield.fields.ColorField(blank=True, default='', image_field=None, max_length=18, samples=[('#ee4545', 'red'), ('#0e70b8', 'blue'), ('#16b06b', 'green'), ('#823dae', 'purple'), ('#e13255', 'pink'), ('#fdf472', 'yellow'), ('#d86900', 'orange'), ('#636363', 'grey')]),
        ),
        migrations.AddField(
            model_name='apptype',
            name='on_accent_color',
            field=models.CharField(choices=[('light', 'light'), ('dark', 'dark')], default='dark', help_text='CSS class for content that appears on top of accent color', max_length=10),
        ),
        migrations.AddField(
            model_name='apptype',
            name='on_primary_color',
            field=models.CharField(choices=[('light', 'light'), ('dark', 'dark')], default='light', help_text='CSS class for content that appears on top of primary color', max_length=10),
        ),
        migrations.AddField(
            model_name='apptype',
            name='primary_color',
            field=colorfield.fields.ColorField(blank=True, default='', image_field=None, max_length=18, samples=[('#ee4545', 'red'), ('#0e70b8', 'blue'), ('#16b06b', 'green'), ('#823dae', 'purple'), ('#e13255', 'pink'), ('#fdf472', 'yellow'), ('#d86900', 'orange'), ('#636363', 'grey')]),
        ),
    ]
