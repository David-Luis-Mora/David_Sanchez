# Generated by Django 5.1.5 on 2025-01-28 19:05

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='color',
            field=colorfield.fields.ColorField(blank=True, default='#ffffff', image_field=None, max_length=25, samples=None),
        ),
    ]
