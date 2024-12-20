# Generated by Django 4.2.16 on 2024-10-22 17:53

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

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
                ("std_fga", models.FloatField()),
                ("std_fta", models.FloatField()),
                ("std_tov", models.FloatField()),
            ],
            options={
                "get_latest_by": "modified",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="RawPlayer",
            fields=[
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
                ("person_id", models.IntegerField(primary_key=True, serialize=False)),
                ("player_last_name", models.CharField(max_length=50)),
                ("player_first_name", models.CharField(max_length=50)),
                ("player_slug", models.CharField(max_length=50)),
                ("team_id", models.IntegerField()),
                ("team_slug", models.CharField(max_length=50, null=True)),
                ("is_defunct", models.IntegerField()),
                ("team_city", models.CharField(max_length=50)),
                ("team_name", models.CharField(max_length=50)),
                ("team_abbreviation", models.CharField(max_length=3)),
                ("jersey_number", models.CharField(max_length=10, null=True)),
                ("position", models.CharField(max_length=10, null=True)),
                ("height", models.CharField(max_length=10, null=True)),
                ("weight", models.CharField(max_length=10, null=True)),
                ("college", models.CharField(max_length=50, null=True)),
                ("country", models.CharField(max_length=50, null=True)),
                ("draft_year", models.IntegerField(null=True)),
                ("draft_round", models.IntegerField(null=True)),
                ("draft_number", models.IntegerField(null=True)),
                ("roster_status", models.IntegerField(null=True)),
            ],
            options={
                "get_latest_by": "modified",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="RawGameLog",
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
                ("player_name", models.CharField(max_length=50)),
                ("nickname", models.CharField(max_length=50)),
                ("team_id", models.IntegerField()),
                ("team_abbreviation", models.CharField(max_length=3)),
                ("team_name", models.CharField(max_length=50)),
                ("game_id", models.CharField(max_length=20)),
                ("game_date", models.CharField()),
                ("matchup", models.CharField(max_length=20)),
                ("wl", models.CharField(max_length=1)),
                ("min", models.FloatField()),
                ("fgm", models.IntegerField()),
                ("fga", models.IntegerField()),
                ("fg_pct", models.FloatField()),
                ("fg3m", models.IntegerField()),
                ("fg3a", models.IntegerField()),
                ("fg3_pct", models.FloatField()),
                ("ftm", models.IntegerField()),
                ("fta", models.IntegerField()),
                ("ft_pct", models.FloatField()),
                ("oreb", models.IntegerField()),
                ("dreb", models.IntegerField()),
                ("reb", models.IntegerField()),
                ("ast", models.IntegerField()),
                ("tov", models.IntegerField()),
                ("stl", models.IntegerField()),
                ("blk", models.IntegerField()),
                ("blka", models.IntegerField()),
                ("pf", models.IntegerField()),
                ("pfd", models.IntegerField()),
                ("pts", models.IntegerField()),
                ("plus_minus", models.IntegerField()),
                ("e_off_rating", models.FloatField()),
                ("off_rating", models.FloatField()),
                ("sp_work_off_rating", models.FloatField()),
                ("e_def_rating", models.FloatField()),
                ("def_rating", models.FloatField()),
                ("sp_work_def_rating", models.FloatField()),
                ("e_net_rating", models.FloatField()),
                ("net_rating", models.FloatField()),
                ("sp_work_net_rating", models.FloatField()),
                ("ast_pct", models.FloatField()),
                ("ast_to", models.FloatField()),
                ("ast_ratio", models.FloatField()),
                ("oreb_pct", models.FloatField()),
                ("dreb_pct", models.FloatField()),
                ("reb_pct", models.FloatField()),
                ("tm_tov_pct", models.FloatField()),
                ("e_tov_pct", models.FloatField()),
                ("efg_pct", models.FloatField()),
                ("ts_pct", models.FloatField()),
                ("usg_pct", models.FloatField()),
                ("e_usg_pct", models.FloatField()),
                ("e_pace", models.FloatField()),
                ("pace", models.FloatField()),
                ("pace_per40", models.FloatField()),
                ("sp_work_pace", models.FloatField()),
                ("pie", models.FloatField()),
                ("poss", models.FloatField()),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["season_year", "player_id", "player_name"],
                        name="games_rawga_season__2dbc59_idx",
                    )
                ],
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
                (
                    "player_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="games.rawplayer",
                    ),
                ),
            ],
            options={
                "get_latest_by": "modified",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="FantasyProjection",
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
                ("min", models.FloatField()),
                ("pts", models.FloatField()),
                ("fg3m", models.FloatField()),
                ("reb", models.FloatField()),
                ("ast", models.FloatField()),
                ("stl", models.FloatField()),
                ("blk", models.FloatField()),
                ("fgm", models.FloatField()),
                ("fga", models.FloatField()),
                ("ftm", models.FloatField()),
                ("fta", models.FloatField()),
                ("tov", models.FloatField()),
                ("usg_pct", models.FloatField()),
                (
                    "player_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="games.rawplayer",
                    ),
                ),
            ],
            options={
                "get_latest_by": "modified",
                "abstract": False,
            },
        ),
    ]
