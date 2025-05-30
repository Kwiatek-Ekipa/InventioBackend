# Generated by Django 5.2 on 2025-05-01 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventio_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='role',
            constraint=models.CheckConstraint(condition=models.Q(('name__in', ['worker', 'technician'])), name='role_name_worker_or_technician'),
        ),
    ]
