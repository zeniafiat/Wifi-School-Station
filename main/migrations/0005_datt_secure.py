# Generated by Django 5.2.1 on 2025-05-27 19:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0004_alter_datt_addr_alter_datt_room"),
    ]

    operations = [
        migrations.AddField(
            model_name="datt",
            name="secure",
            field=models.IntegerField(default=0),
        ),
    ]
