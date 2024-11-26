# Generated by Django 5.0.6 on 2024-11-16 16:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeAPP', '0011_remove_featureproject_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='featureproject',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HomeAPP.project'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HomeAPP.project'),
        ),
        migrations.AlterField(
            model_name='featureproject',
            name='goalAmount',
            field=models.FloatField(default=0.0),
        ),
    ]
