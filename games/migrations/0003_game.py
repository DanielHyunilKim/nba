# Generated by Django 4.2.16 on 2024-10-23 02:13

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ("games", "0002_delete_leagueaverage9cat"),
    ]

    operations = [
        migrations.CreateModel(
            name="Game",
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
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("season_year", models.CharField(max_length=10)),
                ("week_number", models.IntegerField()),
                ("game_date", models.CharField()),
                ("home_team_id", models.IntegerField()),
                ("away_team", models.CharField()),
                ("away_team_id", models.IntegerField()),
            ],
            options={
                "get_latest_by": "modified",
                "abstract": False,
            },
        ),
    ]
