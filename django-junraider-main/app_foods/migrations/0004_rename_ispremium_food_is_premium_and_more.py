# Generated by Django 4.0 on 2023-12-13 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app_foods", "0003_food_description_food_specialprice"),
    ]

    operations = [
        migrations.RenameField(
            model_name="food",
            old_name="isPremium",
            new_name="is_premium",
        ),
        migrations.RenameField(
            model_name="food",
            old_name="promotionEndAt",
            new_name="promotion_end_at",
        ),
        migrations.RenameField(
            model_name="food",
            old_name="specialPrice",
            new_name="special_price",
        ),
    ]
