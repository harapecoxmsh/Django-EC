# Generated by Django 4.2.13 on 2024-06-19 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ecapp", "0006_itemmodel_aold"),
    ]

    operations = [
        migrations.RenameField(
            model_name="itemmodel", old_name="aold", new_name="sold",
        ),
    ]
