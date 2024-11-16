# Generated by Django 5.0.6 on 2024-11-16 16:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeAPP', '0009_alter_donation_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HomeAPP.project'),
        ),
        migrations.AlterField(
            model_name='featureproject',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='HomeAPP.project'),
        ),
    ]
