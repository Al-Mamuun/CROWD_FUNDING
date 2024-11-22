# Generated by Django 5.0.6 on 2024-11-16 08:28

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeAPP', '0005_user_alter_profile_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='donation',
            name='donationDate',
        ),
        migrations.RemoveField(
            model_name='donation',
            name='project',
        ),
        migrations.AddField(
            model_name='donation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='donation',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.ImageField(default='Projectlist/donation.jpeg', upload_to='Projectlist'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
