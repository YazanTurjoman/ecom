# Generated by Django 5.0 on 2024-01-06 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0007_remove_profile_followers_remove_profile_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(blank=True, to='userprofile.profile'),
        ),
    ]
