# Generated by Django 5.0.6 on 2024-11-30 01:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HomeAPP', '0003_comment_user_donation_user_rating_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donation',
            old_name='created_at',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='createdAt',
            new_name='date_created',
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='ratingDate',
            new_name='date',
        ),
        migrations.DeleteModel(
            name='Report',
        ),
    ]