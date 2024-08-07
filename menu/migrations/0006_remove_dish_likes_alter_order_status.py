# Generated by Django 5.0.4 on 2024-07-04 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_like_dish_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='likes',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20),
        ),
    ]
