# Generated by Django 5.0.6 on 2024-11-30 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HomeAPP', '0004_rename_created_at_donation_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donation',
            old_name='date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='date_created',
            new_name='createdAt',
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='date',
            new_name='ratingDate',
        ),
    ]
