# Generated by Django 5.0.6 on 2024-11-23 06:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeAPP', '0023_alter_project_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='HomeAPP.profile'),
        ),
    ]
