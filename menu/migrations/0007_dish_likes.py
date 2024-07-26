# Generated by Django 5.0.4 on 2024-07-04 10:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_remove_dish_likes_alter_order_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='likes',
            field=models.ManyToManyField(related_name='liked_dishes', through='menu.Like', to=settings.AUTH_USER_MODEL),
        ),
    ]
