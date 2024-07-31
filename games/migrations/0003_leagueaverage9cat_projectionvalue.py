# Generated by Django 5.0.6 on 2024-06-11 18:23

import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("games", "0002_fantasyprojection"),
    ]

    operations = [
        migrations.CreateModel(
            name="LeagueAverage9Cat",
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
                ("avg_pts", models.FloatField()),
                ("avg_fg3m", models.FloatField()),
                ("avg_reb", models.FloatField()),
                ("avg_ast", models.FloatField()),
                ("avg_stl", models.FloatField()),
                ("avg_blk", models.FloatField()),
                ("avg_fg_pct", models.FloatField()),
                ("avg_fga", models.FloatField()),
                ("avg_ft_pct", models.FloatField()),
                ("avg_fta", models.FloatField()),
                ("avg_tov", models.FloatField()),
                ("std_pts", models.FloatField()),
                ("std_fg3m", models.FloatField()),
                ("std_reb", models.FloatField()),
                ("std_ast", models.FloatField()),
                ("std_stl", models.FloatField()),
                ("std_blk", models.FloatField()),
                ("std_fg_pct", models.FloatField()),
                ("std_fga", models.FloatField()),
                ("std_ft_pct", models.FloatField()),
                ("std_fta", models.FloatField()),
                ("std_tov", models.FloatField()),
            ],
            options={
                "get_latest_by": "modified",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProjectionValue",
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
                ("player_id", models.IntegerField()),
                ("pts_val", models.FloatField()),
                ("fg3m_val", models.FloatField()),
                ("reb_val", models.FloatField()),
                ("ast_val", models.FloatField()),
                ("stl_val", models.FloatField()),
                ("blk_val", models.FloatField()),
                ("fg_pct_val", models.FloatField()),
                ("ft_pct_val", models.FloatField()),
                ("tov_val", models.FloatField()),
                ("total_val", models.FloatField()),
                ("projection_accuracy", models.FloatField()),
            ],
            options={
                "get_latest_by": "modified",
                "abstract": False,
            },
        ),
    ]
