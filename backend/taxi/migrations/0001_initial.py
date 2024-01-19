# Generated by Django 5.0 on 2024-01-19 12:44

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FixedPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('destination', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PriceDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('satrt', models.DateField()),
                ('finish', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='PriceMile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('date', models.DateField()),
                ('date_return', models.DateField()),
                ('confirmed', models.DateField(auto_now_add=True)),
                ('travel_code', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('origin', models.CharField(max_length=511)),
                ('destination', models.CharField(max_length=511)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JoinedPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.CharField(choices=[('S', 'Sunday'), ('O', 'Otherdays')], max_length=1)),
                ('priceday', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taxi.priceday')),
                ('pricemile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taxi.pricemile')),
            ],
        ),
        migrations.CreateModel(
            name='Travel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('date', models.DateField()),
                ('date_return', models.DateField(blank=True, null=True)),
                ('present', models.DateField(auto_now_add=True)),
                ('travel_code', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('origin', models.CharField(max_length=511)),
                ('destination', models.CharField(max_length=511)),
                ('payment_status', models.CharField(choices=[('P', 'Pending'), ('C', 'Complete'), ('F', 'Failed')], default='P', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]