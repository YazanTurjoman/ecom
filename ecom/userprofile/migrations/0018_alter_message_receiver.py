# Generated by Django 5.0 on 2024-01-09 00:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0017_remove_message_conversation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='userprofile.profile'),
        ),
    ]
