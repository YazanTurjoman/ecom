# Generated by Django 5.0 on 2024-01-10 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_actor_movie_created_at_movie_director_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='slug',
        ),
    ]
