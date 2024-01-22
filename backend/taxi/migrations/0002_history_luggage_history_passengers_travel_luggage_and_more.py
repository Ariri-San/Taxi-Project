# Generated by Django 5.0.1 on 2024-01-21 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='luggage',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='history',
            name='passengers',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='travel',
            name='luggage',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='travel',
            name='passengers',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='pricemile',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]