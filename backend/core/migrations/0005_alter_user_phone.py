# Generated by Django 5.0.1 on 2024-03-13 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_user_phone_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
