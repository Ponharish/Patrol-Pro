# Generated by Django 4.2.13 on 2024-05-31 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="cars",
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
                ("Liscence_Plate", models.CharField(max_length=30)),
                ("status", models.CharField(max_length=30)),
                ("Assigned_Job", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="jobs",
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
                ("status", models.CharField(max_length=30)),
                ("way_points", models.JSONField()),
            ],
        ),
    ]
