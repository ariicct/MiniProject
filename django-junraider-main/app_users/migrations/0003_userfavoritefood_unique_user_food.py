# Generated by Django 4.0.5 on 2023-12-13 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_users", "0002_userfavoritefood_customuser_favorite_food_set_and_more"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="userfavoritefood",
            constraint=models.UniqueConstraint(
                fields=("user", "food"), name="unique_user_food"
            ),
        ),
    ]
