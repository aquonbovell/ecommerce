# Generated by Django 5.0.6 on 2024-06-09 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0003_order_orderitems"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="shipped",
            field=models.BooleanField(default=False),
        ),
    ]
