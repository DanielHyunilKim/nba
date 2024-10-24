# Generated by Django 4.2.16 on 2024-10-23 16:02

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ("games", "0009_alter_fantasyteam_options_alter_game_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="WeeklyTeamGameCount",
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
                ("team_id", models.CharField()),
                ("game_count", models.IntegerField()),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["team_id"], name="games_weekl_team_id_057f2b_idx"
                    )
                ],
            },
        ),
    ]
