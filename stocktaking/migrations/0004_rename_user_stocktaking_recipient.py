# Generated by Django 5.2.1 on 2025-05-25 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocktaking', '0003_alter_stocktaking_release_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stocktaking',
            old_name='user',
            new_name='recipient',
        ),
    ]
