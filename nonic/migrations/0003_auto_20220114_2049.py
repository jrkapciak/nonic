# Generated by Django 3.2.6 on 2022-01-14 19:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nonic", "0002_beer_country"),
    ]

    operations = [
        migrations.AlterField(
            model_name="beer",
            name="code",
            field=models.CharField(max_length=255, unique=True, verbose_name="Code"),
        ),
        migrations.CreateModel(
            name="BeerSource",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("url", models.URLField(unique=True, verbose_name="URL")),
                (
                    "beer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sources",
                        to="nonic.beer",
                        verbose_name="Beer",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]