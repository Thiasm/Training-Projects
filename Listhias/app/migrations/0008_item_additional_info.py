# Generated by Django 5.1.4 on 2025-01-11 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_item_grade_item_release_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='additional_info',
            field=models.JSONField(blank=True, default=1),
            preserve_default=False,
        ),
    ]
