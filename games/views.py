from django.shortcuts import render
from games.models import FantasyProjection, ProjectionValue, RawGameLog, FantasyTeam
from django.core.paginator import Paginator
from games.utils import get_game_counts
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
    return render(request, "games/rankings.html", context)


def rankings(request):
    season_year = "2024-25"

    selected_impact_values = request.GET.getlist("selected_impact_values")
    all_impact_values = [
        "pts_z",
        "fg3m_z",
        "reb_z",
        "ast_z",
        "stl_z",
        "blk_z",
        "fg_pct_z",
        "ft_pct_z",
        "tov_z",
    ]
    if selected_impact_values:
        impact_values = selected_impact_values
    else:
        impact_values = all_impact_values
        selected_impact_values = all_impact_values

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
    game_logs_df = pd.DataFrame.from_records(
        game_logs_qs,
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

    averages_df["pts_z"] = (averages_df["pts"] - league_df["pts"].mean()) / league_df[
        "pts"
    ].std()
    averages_df["fg3m_z"] = (
        averages_df["fg3m"] - league_df["fg3m"].mean()
    ) / league_df["fg3m"].std()
    averages_df["reb_z"] = (averages_df["reb"] - league_df["reb"].mean()) / league_df[
        "reb"
    ].std()
    averages_df["ast_z"] = (averages_df["ast"] - league_df["ast"].mean()) / league_df[
        "ast"
    ].std()
    averages_df["stl_z"] = (averages_df["stl"] - league_df["stl"].mean()) / league_df[
        "stl"
    ].std()
    averages_df["blk_z"] = (averages_df["blk"] - league_df["blk"].mean()) / league_df[
        "blk"
    ].std()
    averages_df["fg_pct_z"] = (
        (averages_df["fg_pct"] - league_avg_fg_pct)
        * averages_df["fga"]
        / league_stddev_fga
    ) / league_stddev_fg_pct
    averages_df["ft_pct_z"] = (
        (averages_df["ft_pct"] - league_avg_ft_pct)
        * averages_df["fta"]
        / league_stddev_fta
    ) / league_stddev_ft_pct
    averages_df["tov_z"] = (
        0 - (averages_df["tov"] - league_df["tov"].mean()) / league_df["tov"].std()
    )

    averages_df["total_z"] = sum([averages_df[x] for x in impact_values])
    averages_df = averages_df.round(decimals=2)
    averages_df.drop(["player_id", "season_year"], axis=1, inplace=True)

    player_impacts = averages_df.to_dict(orient="records")

    # Sorting logic for multiple fields
    sort_by = request.GET.get("sort", "total_z")  # Default sort by total_impact
    direction = request.GET.get("direction", "desc")

    reverse = True if direction == "desc" else False
    player_impacts = sorted(player_impacts, key=lambda x: x[sort_by], reverse=reverse)
    for i, player in enumerate(player_impacts, start=1):
        player["rank"] = i

    # Paginate the sorted player impacts (10 per page for example)
    paginator = Paginator(player_impacts, 100)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "sort_by": sort_by,
        "direction": direction,
        "selected_impact_values": selected_impact_values,
        "all_impact_values": all_impact_values,
    }

    return render(request, "fantasy/rankings.html", context)


def fantasy_matchup(request):
    season_year = "2024-25"
    week = request.GET.get("week")

    if not week:
        week = 1

    teams = FantasyTeam.objects.all()
    team_1_id = request.GET.get("team_1")
    team_2_id = request.GET.get("team_2")

    if not team_1_id or not team_2_id:
        # Default to the first two teams if not selected
        team_1_obj = teams.first()
        team_2_obj = teams.last() if len(teams) > 1 else teams.first()
    else:
        # Query the selected teams from the database
        team_1_obj = FantasyTeam.objects.get(id=team_1_id)
        team_2_obj = FantasyTeam.objects.get(id=team_2_id)

    team_1 = get_game_counts(team_1_obj, week)
    team_2 = get_game_counts(team_2_obj, week)

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

    team_1_df = averages_df[averages_df["player_name"].isin(team_1.keys())]
    team_2_df = averages_df[averages_df["player_name"].isin(team_2.keys())]

    team_1_df["games_played"] = team_1_df["player_name"].map(team_1)
    team_2_df["games_played"] = team_2_df["player_name"].map(team_2)
    team_1_df["fg_pct"] = team_1_df["fgm"] / team_1_df["fga"]
    team_1_df["ft_pct"] = team_1_df["ftm"] / team_1_df["fta"]
    team_2_df["fg_pct"] = team_2_df["fgm"] / team_2_df["fga"]
    team_2_df["ft_pct"] = team_2_df["ftm"] / team_2_df["fta"]
    team_1_df.fillna(0, inplace=True)
    team_2_df.fillna(0, inplace=True)

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
            "week": week,
            "team_1_name": team_1_obj.team_name,
            "team_2_name": team_2_obj.team_name,
            "team_1": team_1,
            "team_2": team_2,
            "weeks": list(range(1, 22)),
            "teams": teams,
            "selected_team_1": team_1_id,
            "selected_team_2": team_2_id,
        },
    )
