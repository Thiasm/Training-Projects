# Generated by Django 5.1.4 on 2025-01-11 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_item_additional_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='api_id',
            field=models.IntegerField(null=True),
        ),
    ]