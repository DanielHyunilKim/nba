# Generated by Django 5.0.6 on 2024-06-11 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("games", "0003_leagueaverage9cat_projectionvalue"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="leagueaverage9cat",
            name="std_fg_pct",
        ),
        migrations.RemoveField(
            model_name="leagueaverage9cat",
            name="std_ft_pct",
        ),
    ]
