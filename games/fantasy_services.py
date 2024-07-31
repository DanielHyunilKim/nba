from django.db.models import QuerySet
from games.models import RawGameLog

import pandas as pd

"""
season, player, team_abbreviation, game_date, matchup, min, pt, 3, reb, ast, stl, blk, fg%, fga, ft%, fta, to, usg
games = queryset of RawGameLogs
"""
def get_9_cat(games: QuerySet):
    df = pd.DataFrame.from_records(
        games.values(
            "season_year",
            "player_name",
            "team_abbreviation",
            "game_date",
            "matchup",
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
            "usg_pct"
        )
    )
    return df

