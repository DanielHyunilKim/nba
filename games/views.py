from django.shortcuts import render
from games.models import FantasyProjection, ProjectionValue, RawGameLog, FantasyTeam
from django.core.paginator import Paginator
import pandas as pd


# Create your views here.
def projections(request):
    player_ids = [
        projection.player_id for projection in FantasyProjection.objects.all()
    ]
    projections = FantasyProjection.objects.filter(season_year="2024-25")
    projection_values = ProjectionValue.objects.filter(season_year="2024-25")

    projection_paginator = Paginator(projections, 20)
    page_number = request.GET.get("page")
    page_obj = projection_paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "projection_values": projection_values,
        "player_ids": player_ids,
    }
    return render(request, "games/index.html", context)


def fantasy(request):
    season_year = "2023-24"

    game_logs_qs = RawGameLog.objects.filter(season_year=season_year).values_list(
        "player_id",
        "player_name",
        "season_year",
        "min",
        "pts",
        "fg3m",
        "reb",
        "ast",
        "stl",
        "blk",
        "fgm",
        "fga",
        "ftm",
        "fta",
        "tov",
        "usg_pct",
    )
    game_logs_df = pd.DataFrame(
        list(game_logs_qs),
        columns=[
            "player_id",
            "player_name",
            "season_year",
            "min",
            "pts",
            "fg3m",
            "reb",
            "ast",
            "stl",
            "blk",
            "fgm",
            "fga",
            "ftm",
            "fta",
            "tov",
            "usg_pct",
        ],
    )
    averages_df = (
        game_logs_df.groupby(["player_id", "player_name", "season_year"])
        .agg(
            {
                "min": "mean",
                "pts": "mean",
                "fg3m": "mean",
                "reb": "mean",
                "ast": "mean",
                "stl": "mean",
                "blk": "mean",
                "fgm": "mean",
                "fga": "mean",
                "ftm": "mean",
                "fta": "mean",
                "tov": "mean",
                "usg_pct": "mean",
            }
        )
        .reset_index()
    )

    # league average for players playing > 15 minutes
    league_df = averages_df[averages_df["min"] >= 15]
    averages_df["fg_pct"] = averages_df["fgm"] / averages_df["fga"]
    averages_df["ft_pct"] = averages_df["ftm"] / averages_df["fta"]
    averages_df.fillna(0, inplace=True)
    league_avg_fg_pct = league_df["fgm"].sum() / league_df["fga"].sum()
    league_stddev_fg_pct = (league_df["fgm"] / league_df["fga"]).std()
    league_avg_ft_pct = league_df["ftm"].sum() / league_df["fta"].sum()
    league_stddev_ft_pct = (league_df["ftm"] / league_df["fta"]).std()
    league_stddev_fga = league_df["fga"].std()
    league_stddev_fta = league_df["fta"].std()

    averages_df["pts_val"] = (averages_df["pts"] - league_df["pts"].mean()) / league_df[
        "pts"
    ].std()
    averages_df["fg3m_val"] = (
        averages_df["fg3m"] - league_df["fg3m"].mean()
    ) / league_df["fg3m"].std()
    averages_df["reb_val"] = (averages_df["reb"] - league_df["reb"].mean()) / league_df[
        "reb"
    ].std()
    averages_df["ast_val"] = (averages_df["ast"] - league_df["ast"].mean()) / league_df[
        "ast"
    ].std()
    averages_df["stl_val"] = (averages_df["stl"] - league_df["stl"].mean()) / league_df[
        "stl"
    ].std()
    averages_df["blk_val"] = (averages_df["blk"] - league_df["blk"].mean()) / league_df[
        "blk"
    ].std()
    averages_df["fg_pct_val"] = (
        (averages_df["fg_pct"] - league_avg_fg_pct)
        * averages_df["fga"]
        / league_stddev_fga
    ) / league_stddev_fg_pct
    averages_df["ft_pct_val"] = (
        (averages_df["ft_pct"] - league_avg_ft_pct)
        * averages_df["fta"]
        / league_stddev_fta
    ) / league_stddev_ft_pct
    averages_df["tov_val"] = (
        0 - (averages_df["tov"] - league_df["tov"].mean()) / league_df["tov"].std()
    )

    averages_df["total_impact"] = (
        averages_df["pts_val"]
        + averages_df["fg3m_val"]
        + averages_df["reb_val"]
        + averages_df["ast_val"]
        + averages_df["stl_val"]
        + averages_df["blk_val"]
        + averages_df["fg_pct_val"]
        + averages_df["ft_pct_val"]
        + averages_df["tov_val"]
    )
    averages_df = averages_df.round(decimals=2)
    averages_df.drop("player_id", axis=1, inplace=True)
    averages_df.rename(columns={"season_year": "season"}, inplace=True)
    averages_df["season"] = "2024"

    player_impacts = averages_df.to_dict(orient="records")

    # Sorting logic for multiple fields
    sort_by = request.GET.get("sort", "total_impact")  # Default sort by total_impact
    direction = request.GET.get("direction", "desc")

    reverse = True if direction == "desc" else False
    player_impacts = sorted(player_impacts, key=lambda x: x[sort_by], reverse=reverse)

    # Paginate the sorted player impacts (10 per page for example)
    paginator = Paginator(player_impacts, 100)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "sort_by": sort_by,
        "direction": direction,
    }

    return render(request, "fantasy/index.html", context)


def fantasy_matchup(request):
    season_year = "2023-24"
    week = 1
    team_1 = FantasyTeam.get(team_name="Slam Dunkin")
    team_2 = FantasyTeam.get(team_name="Kawhi Baby")

    team_1 = {
        "Donovan Mitchell": 3,
        "Scottie Barnes": 3,
        "Kyrie Irving": 2,
        "Jalen Williams": 3,
        "Fred VanVleet": 3,
        "Franz Wagner": 3,
        "Isaiah Hartenstein": 0,
        "Tobias Harris": 3,
        "Ivica Zubac": 3,
        "Zach Edey": 3,
        "Trey Murphy III": 0,
        "Tyus Jones": 3,
        "Gary Trent Jr.": 3,
        "Dalton Knecht": 2,
    }
    team_2 = {
        "Dejounte Murray": 3,
        "Anthony Edwards": 3,
        "Michael Porter Jr.": 2,
        "Keegan Murray": 2,
        "Domantas Sabonis": 2,
        "Immanuel Quickley": 3,
        "Jerami Grant": 3,
        "Bam Adebayo": 2,
        "Tyler Herro": 2,
        "Josh Hart": 2,
        "Brandin Podziemski": 3,
        "Malik Monk": 2,
        "Jordan Clarkson": 2,
    }

    rostered_players = list(team_1.keys()) + list(team_2.keys())

    game_logs_qs = RawGameLog.objects.filter(
        season_year=season_year, player_name__in=rostered_players
    ).values_list(
        "player_id",
        "player_name",
        "season_year",
        "min",
        "pts",
        "fg3m",
        "reb",
        "ast",
        "stl",
        "blk",
        "fgm",
        "fga",
        "ftm",
        "fta",
        "tov",
        "usg_pct",
    )
    game_logs_df = pd.DataFrame(
        list(game_logs_qs),
        columns=[
            "player_id",
            "player_name",
            "season_year",
            "min",
            "pts",
            "fg3m",
            "reb",
            "ast",
            "stl",
            "blk",
            "fgm",
            "fga",
            "ftm",
            "fta",
            "tov",
            "usg_pct",
        ],
    )
    averages_df = (
        game_logs_df.groupby(["player_id", "player_name", "season_year"])
        .agg(
            {
                "min": "mean",
                "pts": "mean",
                "fg3m": "mean",
                "reb": "mean",
                "ast": "mean",
                "stl": "mean",
                "blk": "mean",
                "fgm": "mean",
                "fga": "mean",
                "ftm": "mean",
                "fta": "mean",
                "tov": "mean",
                "usg_pct": "mean",
            }
        )
        .reset_index()
    )

    edey_df = pd.DataFrame(
        [
            {
                "player_id": 1641744,
                "player_name": "Zach Edey",
                "season_year": "2024-25",
                "min": 25,
                "pts": 12,
                "fg3m": 0,
                "reb": 9,
                "ast": 1.5,
                "stl": 0.2,
                "blk": 1.5,
                "fgm": 4.5,
                "fga": 8,
                "ftm": 2.1,
                "fta": 3,
                "tov": 2,
                "usg_pct": 0.18,
            }
        ]
    )

    knecht_df = pd.DataFrame(
        [
            {
                "player_id": 1642261,
                "player_name": "Dalton Knecht",
                "season_year": "2024-25",
                "min": 20,
                "pts": 10,
                "fg3m": 2,
                "reb": 3,
                "ast": 1.5,
                "stl": 0.4,
                "blk": 0.4,
                "fgm": 3,
                "fga": 7,
                "ftm": 1.6,
                "fta": 2.1,
                "tov": 1.5,
                "usg_pct": 0.18,
            }
        ]
    )

    team_1_df = averages_df[averages_df["player_name"].isin(team_1.keys())]
    team_1_df = pd.concat([team_1_df, edey_df, knecht_df])
    team_2_df = averages_df[averages_df["player_name"].isin(team_2.keys())]

    team_1_df["games_played"] = team_1_df["player_name"].map(team_1)
    team_2_df["games_played"] = team_2_df["player_name"].map(team_2)
    team_1_df["fg_pct"] = team_1_df["fgm"] / team_1_df["fga"]
    team_1_df["ft_pct"] = team_1_df["ftm"] / team_1_df["fta"]
    team_2_df["fg_pct"] = team_2_df["fgm"] / team_2_df["fga"]
    team_2_df["ft_pct"] = team_2_df["ftm"] / team_2_df["fta"]

    team_totals = []

    for team in (team_1_df, team_2_df):
        min = ((team["min"] * team["games_played"]).sum(),)
        pts = ((team["pts"] * team["games_played"]).sum(),)
        fg3m = ((team["fg3m"] * team["games_played"]).sum(),)
        reb = ((team["reb"] * team["games_played"]).sum(),)
        ast = ((team["ast"] * team["games_played"]).sum(),)
        stl = ((team["stl"] * team["games_played"]).sum(),)
        blk = ((team["blk"] * team["games_played"]).sum(),)
        fgm = ((team["fgm"] * team["games_played"]).sum(),)
        fga = ((team["fga"] * team["games_played"]).sum(),)
        fg_pct = fgm[0] / fga[0]
        ftm = ((team["ftm"] * team["games_played"]).sum(),)
        fta = ((team["fta"] * team["games_played"]).sum(),)
        ft_pct = ftm[0] / fta[0]
        tov = ((team["tov"] * team["games_played"]).sum(),)
        games_played = team["games_played"].sum()

        totals = pd.DataFrame(
            [
                {
                    "player_id": None,
                    "player_name": "Total",
                    "season_year": "2024-25",
                    "min": min[0],
                    "pts": pts[0],
                    "fg3m": fg3m[0],
                    "reb": reb[0],
                    "ast": ast[0],
                    "stl": stl[0],
                    "blk": blk[0],
                    "fgm": fgm[0],
                    "fga": fga[0],
                    "fg_pct": fg_pct,
                    "ftm": ftm[0],
                    "fta": fta[0],
                    "ft_pct": ft_pct,
                    "tov": tov[0],
                    "usg_pct": None,
                    "games_played": games_played,
                }
            ]
        )
        team = pd.concat([team, totals], ignore_index=True)
        team.reset_index(inplace=True)
        cols = [
            "player_name",
            "min",
            "pts",
            "fg3m",
            "reb",
            "ast",
            "stl",
            "blk",
            "fgm",
            "fga",
            "fg_pct",
            "ftm",
            "fta",
            "ft_pct",
            "tov",
            "games_played",
        ]
        team = team[cols]
        team_totals.append(team)

    team_totals = [team_total.round(decimals=3) for team_total in team_totals]
    team_1 = team_totals[0].to_dict(orient="records")
    team_2 = team_totals[1].to_dict(orient="records")

    return render(
        request,
        "fantasy/matchup.html",
        {
            "team_1": team_1,
            "team_2": team_2,
        },
    )
