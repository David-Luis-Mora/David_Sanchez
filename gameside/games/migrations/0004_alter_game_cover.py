# Generated by Django 5.1.5 on 2025-01-28 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_alter_game_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='cover',
            field=models.ImageField(blank=True, default='covers/default.jpg', upload_to=''),
        ),
    ]
