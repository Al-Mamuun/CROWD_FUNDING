# Generated by Django 5.0.6 on 2024-11-23 06:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeAPP', '0022_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='HomeAPP.profile'),
        ),
    ]