# Generated by Django 5.1.5 on 2025-01-27 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_alter_game_pegi'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='user',
            new_name='author',
        ),
    ]
