# Generated by Django 5.0 on 2024-01-03 06:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_customer_user_product_likes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='product_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
