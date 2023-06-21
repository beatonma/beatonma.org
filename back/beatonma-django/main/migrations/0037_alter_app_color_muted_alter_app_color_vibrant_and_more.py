# Generated by Django 4.1.5 on 2023-04-18 17:18

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_rename_primary_color_app_color_muted_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='color_muted',
            field=colorfield.fields.ColorField(blank=True, default='', image_field=None, max_length=18, samples=[('#ee4545', '#ee4545'), ('#0e70b8', '#0e70b8'), ('#16b06b', '#16b06b'), ('#823dae', '#823dae'), ('#e13255', '#e13255'), ('#fdf472', '#fdf472'), ('#d86900', '#d86900'), ('#636363', '#636363'), ('#ff6d60', '#ff6d60'), ('#f7d060', '#f7d060'), ('#f3e99f', '#f3e99f'), ('#98d8aa', '#98d8aa'), ('#3c486b', '#3c486b'), ('#f0f0f0', '#f0f0f0'), ('#f9d949', '#f9d949'), ('#f45050', '#f45050'), ('#4d455d', '#4d455d'), ('#e96479', '#e96479'), ('#f5e9cf', '#f5e9cf'), ('#7db9b6', '#7db9b6'), ('#0a4d68', '#0a4d68'), ('#088395', '#088395'), ('#05bfdb', '#05bfdb'), ('#00ffca', '#00ffca'), ('#2c3333', '#2c3333'), ('#2e4f4f', '#2e4f4f'), ('#0e8388', '#0e8388'), ('#cbe4de', '#cbe4de'), ('#181823', '#181823'), ('#537fe7', '#537fe7'), ('#c0eef2', '#c0eef2'), ('#e9f8f9', '#e9f8f9'), ('#483838', '#483838'), ('#42855b', '#42855b'), ('#90b77d', '#90b77d'), ('#d2d79f', '#d2d79f')]),
        ),
        migrations.AlterField(
            model_name='app',
            name='color_vibrant',
            field=colorfield.fields.ColorField(blank=True, default='', image_field=None, max_length=18, samples=[('#ee4545', '#ee4545'), ('#0e70b8', '#0e70b8'), ('#16b06b', '#16b06b'), ('#823dae', '#823dae'), ('#e13255', '#e13255'), ('#fdf472', '#fdf472'), ('#d86900', '#d86900'), ('#636363', '#636363'), ('#ff6d60', '#ff6d60'), ('#f7d060', '#f7d060'), ('#f3e99f', '#f3e99f'), ('#98d8aa', '#98d8aa'), ('#3c486b', '#3c486b'), ('#f0f0f0', '#f0f0f0'), ('#f9d949', '#f9d949'), ('#f45050', '#f45050'), ('#4d455d', '#4d455d'), ('#e96479', '#e96479'), ('#f5e9cf', '#f5e9cf'), ('#7db9b6', '#7db9b6'), ('#0a4d68', '#0a4d68'), ('#088395', '#088395'), ('#05bfdb', '#05bfdb'), ('#00ffca', '#00ffca'), ('#2c3333', '#2c3333'), ('#2e4f4f', '#2e4f4f'), ('#0e8388', '#0e8388'), ('#cbe4de', '#cbe4de'), ('#181823', '#181823'), ('#537fe7', '#537fe7'), ('#c0eef2', '#c0eef2'), ('#e9f8f9', '#e9f8f9'), ('#483838', '#483838'), ('#42855b', '#42855b'), ('#90b77d', '#90b77d'), ('#d2d79f', '#d2d79f')]),
        ),
        migrations.AlterField(
            model_name='apptype',
            name='color_muted',
            field=colorfield.fields.ColorField(blank=True, default='', image_field=None, max_length=18, samples=[('#ee4545', '#ee4545'), ('#0e70b8', '#0e70b8'), ('#16b06b', '#16b06b'), ('#823dae', '#823dae'), ('#e13255', '#e13255'), ('#fdf472', '#fdf472'), ('#d86900', '#d86900'), ('#636363', '#636363'), ('#ff6d60', '#ff6d60'), ('#f7d060', '#f7d060'), ('#f3e99f', '#f3e99f'), ('#98d8aa', '#98d8aa'), ('#3c486b', '#3c486b'), ('#f0f0f0', '#f0f0f0'), ('#f9d949', '#f9d949'), ('#f45050', '#f45050'), ('#4d455d', '#4d455d'), ('#e96479', '#e96479'), ('#f5e9cf', '#f5e9cf'), ('#7db9b6', '#7db9b6'), ('#0a4d68', '#0a4d68'), ('#088395', '#088395'), ('#05bfdb', '#05bfdb'), ('#00ffca', '#00ffca'), ('#2c3333', '#2c3333'), ('#2e4f4f', '#2e4f4f'), ('#0e8388', '#0e8388'), ('#cbe4de', '#cbe4de'), ('#181823', '#181823'), ('#537fe7', '#537fe7'), ('#c0eef2', '#c0eef2'), ('#e9f8f9', '#e9f8f9'), ('#483838', '#483838'), ('#42855b', '#42855b'), ('#90b77d', '#90b77d'), ('#d2d79f', '#d2d79f')]),
        ),
        migrations.AlterField(
            model_name='apptype',
            name='color_vibrant',
            field=colorfield.fields.ColorField(blank=True, default='', image_field=None, max_length=18, samples=[('#ee4545', '#ee4545'), ('#0e70b8', '#0e70b8'), ('#16b06b', '#16b06b'), ('#823dae', '#823dae'), ('#e13255', '#e13255'), ('#fdf472', '#fdf472'), ('#d86900', '#d86900'), ('#636363', '#636363'), ('#ff6d60', '#ff6d60'), ('#f7d060', '#f7d060'), ('#f3e99f', '#f3e99f'), ('#98d8aa', '#98d8aa'), ('#3c486b', '#3c486b'), ('#f0f0f0', '#f0f0f0'), ('#f9d949', '#f9d949'), ('#f45050', '#f45050'), ('#4d455d', '#4d455d'), ('#e96479', '#e96479'), ('#f5e9cf', '#f5e9cf'), ('#7db9b6', '#7db9b6'), ('#0a4d68', '#0a4d68'), ('#088395', '#088395'), ('#05bfdb', '#05bfdb'), ('#00ffca', '#00ffca'), ('#2c3333', '#2c3333'), ('#2e4f4f', '#2e4f4f'), ('#0e8388', '#0e8388'), ('#cbe4de', '#cbe4de'), ('#181823', '#181823'), ('#537fe7', '#537fe7'), ('#c0eef2', '#c0eef2'), ('#e9f8f9', '#e9f8f9'), ('#483838', '#483838'), ('#42855b', '#42855b'), ('#90b77d', '#90b77d'), ('#d2d79f', '#d2d79f')]),
        ),
        migrations.AlterField(
            model_name='article',
            name='color_muted',
            field=colorfield.fields.ColorField(blank=True, default='', image_field=None, max_length=18, samples=[('#ee4545', '#ee4545'), ('#0e70b8', '#0e70b8'), ('#16b06b', '#16b06b'), ('#823dae', '#823dae'), ('#e13255', '#e13255'), ('#fdf472', '#fdf472'), ('#d86900', '#d86900'), ('#636363', '#636363'), ('#ff6d60', '#ff6d60'), ('#f7d060', '#f7d060'), ('#f3e99f', '#f3e99f'), ('#98d8aa', '#98d8aa'), ('#3c486b', '#3c486b'), ('#f0f0f0', '#f0f0f0'), ('#f9d949', '#f9d949'), ('#f45050', '#f45050'), ('#4d455d', '#4d455d'), ('#e96479', '#e96479'), ('#f5e9cf', '#f5e9cf'), ('#7db9b6', '#7db9b6'), ('#0a4d68', '#0a4d68'), ('#088395', '#088395'), ('#05bfdb', '#05bfdb'), ('#00ffca', '#00ffca'), ('#2c3333', '#2c3333'), ('#2e4f4f', '#2e4f4f'), ('#0e8388', '#0e8388'), ('#cbe4de', '#cbe4de'), ('#181823', '#181823'), ('#537fe7', '#537fe7'), ('#c0eef2', '#c0eef2'), ('#e9f8f9', '#e9f8f9'), ('#483838', '#483838'), ('#42855b', '#42855b'), ('#90b77d', '#90b77d'), ('#d2d79f', '#d2d79f')]),
        ),
        migrations.AlterField(
            model_name='article',
            name='color_vibrant',
            field=colorfield.fields.ColorField(blank=True, default='', image_field=None, max_length=18, samples=[('#ee4545', '#ee4545'), ('#0e70b8', '#0e70b8'), ('#16b06b', '#16b06b'), ('#823dae', '#823dae'), ('#e13255', '#e13255'), ('#fdf472', '#fdf472'), ('#d86900', '#d86900'), ('#636363', '#636363'), ('#ff6d60', '#ff6d60'), ('#f7d060', '#f7d060'), ('#f3e99f', '#f3e99f'), ('#98d8aa', '#98d8aa'), ('#3c486b', '#3c486b'), ('#f0f0f0', '#f0f0f0'), ('#f9d949', '#f9d949'), ('#f45050', '#f45050'), ('#4d455d', '#4d455d'), ('#e96479', '#e96479'), ('#f5e9cf', '#f5e9cf'), ('#7db9b6', '#7db9b6'), ('#0a4d68', '#0a4d68'), ('#088395', '#088395'), ('#05bfdb', '#05bfdb'), ('#00ffca', '#00ffca'), ('#2c3333', '#2c3333'), ('#2e4f4f', '#2e4f4f'), ('#0e8388', '#0e8388'), ('#cbe4de', '#cbe4de'), ('#181823', '#181823'), ('#537fe7', '#537fe7'), ('#c0eef2', '#c0eef2'), ('#e9f8f9', '#e9f8f9'), ('#483838', '#483838'), ('#42855b', '#42855b'), ('#90b77d', '#90b77d'), ('#d2d79f', '#d2d79f')]),
        ),
        migrations.AlterField(
            model_name='blog',
            name='color_muted',
            field=colorfield.fields.ColorField(blank=True, default='', image_field=None, max_length=18, samples=[('#ee4545', '#ee4545'), ('#0e70b8', '#0e70b8'), ('#16b06b', '#16b06b'), ('#823dae', '#823dae'), ('#e13255', '#e13255'), ('#fdf472', '#fdf472'), ('#d86900', '#d86900'), ('#636363', '#636363'), ('#ff6d60', '#ff6d60'), ('#f7d060', '#f7d060'), ('#f3e99f', '#f3e99f'), ('#98d8aa', '#98d8aa'), ('#3c486b', '#3c486b'), ('#f0f0f0', '#f0f0f0'), ('#f9d949', '#f9d949'), ('#f45050', '#f45050'), ('#4d455d', '#4d455d'), ('#e96479', '#e96479'), ('#f5e9cf', '#f5e9cf'), ('#7db9b6', '#7db9b6'), ('#0a4d68', '#0a4d68'), ('#088395', '#088395'), ('#05bfdb', '#05bfdb'), ('#00ffca', '#00ffca'), ('#2c3333', '#2c3333'), ('#2e4f4f', '#2e4f4f'), ('#0e8388', '#0e8388'), ('#cbe4de', '#cbe4de'), ('#181823', '#181823'), ('#537fe7', '#537fe7'), ('#c0eef2', '#c0eef2'), ('#e9f8f9', '#e9f8f9'), ('#483838', '#483838'), ('#42855b', '#42855b'), ('#90b77d', '#90b77d'), ('#d2d79f', '#d2d79f')]),
        ),
        migrations.AlterField(
            model_name='blog',
            name='color_vibrant',
            field=colorfield.fields.ColorField(blank=True, default='', image_field=None, max_length=18, samples=[('#ee4545', '#ee4545'), ('#0e70b8', '#0e70b8'), ('#16b06b', '#16b06b'), ('#823dae', '#823dae'), ('#e13255', '#e13255'), ('#fdf472', '#fdf472'), ('#d86900', '#d86900'), ('#636363', '#636363'), ('#ff6d60', '#ff6d60'), ('#f7d060', '#f7d060'), ('#f3e99f', '#f3e99f'), ('#98d8aa', '#98d8aa'), ('#3c486b', '#3c486b'), ('#f0f0f0', '#f0f0f0'), ('#f9d949', '#f9d949'), ('#f45050', '#f45050'), ('#4d455d', '#4d455d'), ('#e96479', '#e96479'), ('#f5e9cf', '#f5e9cf'), ('#7db9b6', '#7db9b6'), ('#0a4d68', '#0a4d68'), ('#088395', '#088395'), ('#05bfdb', '#05bfdb'), ('#00ffca', '#00ffca'), ('#2c3333', '#2c3333'), ('#2e4f4f', '#2e4f4f'), ('#0e8388', '#0e8388'), ('#cbe4de', '#cbe4de'), ('#181823', '#181823'), ('#537fe7', '#537fe7'), ('#c0eef2', '#c0eef2'), ('#e9f8f9', '#e9f8f9'), ('#483838', '#483838'), ('#42855b', '#42855b'), ('#90b77d', '#90b77d'), ('#d2d79f', '#d2d79f')]),
        ),
    ]
