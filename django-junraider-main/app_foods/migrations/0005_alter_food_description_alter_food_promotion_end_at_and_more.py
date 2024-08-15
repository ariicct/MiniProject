# Generated by Django 4.0 on 2023-12-13 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_foods", "0004_rename_ispremium_food_is_premium_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="food",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="food",
            name="promotion_end_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="food",
            name="special_price",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
