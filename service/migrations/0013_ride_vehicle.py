# Generated by Django 4.2.7 on 2024-02-09 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("service", "0012_alter_page_options_invoice_vehicle"),
    ]

    operations = [
        migrations.AddField(
            model_name="ride",
            name="vehicle",
            field=models.CharField(
                choices=[
                    ("voiture", "voiture"),
                    ("mini-bus", "mini-bus"),
                    ("jeep 4x4", "jeep 4x4"),
                ],
                default="voiture",
                max_length=100,
                verbose_name="vehicule",
            ),
        ),
    ]
