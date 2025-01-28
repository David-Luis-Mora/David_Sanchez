# Generated by Django 5.1.5 on 2025-01-28 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'Initiated'), (1, 'Confirmed'), (2, 'Cancelled'), (3, 'Paid')], default=0),
        ),
    ]
