# Generated by Django 5.1.5 on 2025-01-28 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Initiated'), (2, 'Confirmed'), (-1, 'Cancelled'), (3, 'Paid')], default=1),
        ),
    ]
