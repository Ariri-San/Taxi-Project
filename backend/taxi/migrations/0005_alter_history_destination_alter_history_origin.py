# Generated by Django 5.0.1 on 2024-03-13 12:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxi', '0004_location_alter_travel_destination_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_destination', to='taxi.location'),
        ),
        migrations.AlterField(
            model_name='history',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_origin', to='taxi.location'),
        ),
    ]
