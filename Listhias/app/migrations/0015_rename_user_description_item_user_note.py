# Generated by Django 5.1.4 on 2025-01-14 02:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_item_user_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='user_description',
            new_name='user_note',
        ),
    ]