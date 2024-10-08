# Generated by Django 4.0.5 on 2023-12-13 09:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app_foods", "0006_food_image_relative_url"),
        ("app_users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserFavoriteFood",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "level",
                    models.SmallIntegerField(
                        choices=[(1, "ชอบ"), (2, "ชอบมาก"), (3, "ชอบโคตร")], default=1
                    ),
                ),
                (
                    "food",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="favorited_user_pivot_set",
                        to="app_foods.food",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="customuser",
            name="favorite_food_set",
            field=models.ManyToManyField(
                related_name="favorited_user_set",
                through="app_users.UserFavoriteFood",
                to="app_foods.food",
            ),
        ),
        migrations.AddField(
            model_name="userfavoritefood",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="favorite_food_pivot_set",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
