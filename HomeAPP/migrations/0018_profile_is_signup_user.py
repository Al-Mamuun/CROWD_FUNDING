# Generated by Django 5.0.6 on 2024-11-23 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeAPP', '0017_profile_phn_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_signup_user',
            field=models.BooleanField(default=False),
        ),
    ]
