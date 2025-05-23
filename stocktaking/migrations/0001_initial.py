# Generated by Django 5.1.7 on 2025-04-14 19:55

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hardware', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Stocktaking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('release_date', models.DateTimeField(auto_now_add=True)),
                ('return_date', models.DateTimeField(blank=True, null=True)),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hardware.device')),
                ('released_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='released_by_stocktaking', to=settings.AUTH_USER_MODEL)),
                ('returned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='returned_by_stocktaking', to=settings.AUTH_USER_MODEL)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_stocktaking', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
