# Generated by Django 4.2.13 on 2024-06-04 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ecapp", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="itemmodel", name="comment",),
        migrations.DeleteModel(name="Comment",),
    ]