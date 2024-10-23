from django.db import transaction
from games.models import RawPlayer, RawGameLog, FantasyProjection, ProjectionValue, Game
import pandas as pd
from tqdm import tqdm
import numpy as np


from logging import getLogger

log = getLogger(__name__)

PLAYER_FIELDS = [
    'PERSON_ID',
    'PLAYER_LAST_NAME',
    'PLAYER_FIRST_NAME',
    'PLAYER_SLUG',
    'TEAM_ID',
    'TEAM_SLUG',
    'IS_DEFUNCT',
    'TEAM_CITY',
    'TEAM_NAME',
    'TEAM_ABBREVIATION',
    'JERSEY_NUMBER',
    'POSITION',
    'HEIGHT',
    'WEIGHT',
    'COLLEGE',
    'COUNTRY',
    'DRAFT_YEAR',
    'DRAFT_ROUND',
    'DRAFT_NUMBER',
    'ROSTER_STATUS'
]

TRAD_FIELDS = [
    "SEASON_YEAR",
    "PLAYER_ID",
    "PLAYER_NAME",
    "NICKNAME",
    "TEAM_ID",
    "TEAM_ABBREVIATION",
    "TEAM_NAME",
    "GAME_ID",
    "GAME_DATE",
    "MATCHUP",
    "WL",
    "MIN",
    "FGM",
    "FGA",
    "FG_PCT",
    "FG3M",
    "FG3A",
    "FG3_PCT",
    "FTM",
    "FTA",
    "FT_PCT",
    "OREB",
    "DREB",
    "REB",
    "AST",
    "TOV",
    "STL",
    "BLK",
    "BLKA",
    "PF",
    "PFD",
    "PTS",
    "PLUS_MINUS",
]

ADV_FIELDS = [
    "SEASON_YEAR",
    "PLAYER_ID",
    "GAME_ID",
    "E_OFF_RATING",
    "OFF_RATING",
    "sp_work_OFF_RATING",
    "E_DEF_RATING",
    "DEF_RATING",
    "sp_work_DEF_RATING",
    "E_NET_RATING",
    "NET_RATING",
    "sp_work_NET_RATING",
    "AST_PCT",
    "AST_TO",
    "AST_RATIO",
    "OREB_PCT",
    "DREB_PCT",
    "REB_PCT",
    "TM_TOV_PCT",
    "E_TOV_PCT",
    "EFG_PCT",
    "TS_PCT",
    "USG_PCT",
    "E_USG_PCT",
    "E_PACE",
    "PACE",
    "PACE_PER40",
    "sp_work_PACE",
    "PIE",
    "POSS",
]


def handle_players(players):
    headers = players["resultSets"][0]["headers"]
    data = players["resultSets"][0]["rowSet"]
    df = pd.DataFrame(columns=headers, data=data)
    df = df.replace({np.nan: None})
    df_pruned = df[PLAYER_FIELDS]

    player_objs = [
        RawPlayer(
            person_id=row['PERSON_ID'],
            player_last_name=row['PLAYER_LAST_NAME'],
            player_first_name=row['PLAYER_FIRST_NAME'],
            player_slug=row['PLAYER_SLUG'],
            team_id=row['TEAM_ID'],
            team_slug=row['TEAM_SLUG'],
            is_defunct=row['IS_DEFUNCT'],
            team_city=row['TEAM_CITY'],
            team_name=row['TEAM_NAME'],
            team_abbreviation=row['TEAM_ABBREVIATION'],
            jersey_number=row['JERSEY_NUMBER'],
            position=row['POSITION'],
            height=row['HEIGHT'],
            weight=row['WEIGHT'],
            college=row['COLLEGE'],
            country=row['COUNTRY'],
            draft_year=row['DRAFT_YEAR'],
            draft_round=row['DRAFT_ROUND'],
            draft_number=row['DRAFT_NUMBER'],
            roster_status=row['ROSTER_STATUS'],
        )
        for _, row in tqdm(df_pruned.iterrows())
    ]

    # Use a transaction to ensure atomicity and performance
    with transaction.atomic():
        RawPlayer.objects.all().delete()  # Clear existing data
        RawPlayer.objects.bulk_create(player_objs, batch_size=1000)


def handle_game_logs(traditional, advanced):

    if validate_gamelog_json(traditional, advanced):

        trad_headers = traditional["resultSets"][0]["headers"]
        trad_data = traditional["resultSets"][0]["rowSet"]

        adv_headers = advanced["resultSets"][0]["headers"]
        adv_data = advanced["resultSets"][0]["rowSet"]

        trad_df = pd.DataFrame(columns=trad_headers, data=trad_data)
        adv_df = pd.DataFrame(columns=adv_headers, data=adv_data)
        trad_df_pruned = trad_df[TRAD_FIELDS]
        adv_df_pruned = adv_df[ADV_FIELDS]

        combined_df = pd.merge(
            left=trad_df_pruned,
            right=adv_df_pruned,
            how="inner",
            on=[
                "SEASON_YEAR",
                "PLAYER_ID",
                "GAME_ID",
            ],
        )

        gamelog_objs = [
            RawGameLog(
                season_year=row["SEASON_YEAR"],
                player_id=row["PLAYER_ID"],
                player_name=row["PLAYER_NAME"],
                nickname=row["NICKNAME"],
                team_id=row["TEAM_ID"],
                team_abbreviation=row["TEAM_ABBREVIATION"],
                team_name=row["TEAM_NAME"],
                game_id=row["GAME_ID"],
                game_date=row["GAME_DATE"],
                matchup=row["MATCHUP"],
                wl=row["WL"],
                min=row["MIN"],
                fgm=row["FGM"],
                fga=row["FGA"],
                fg_pct=row["FG_PCT"],
                fg3m=row["FG3M"],
                fg3a=row["FG3A"],
                fg3_pct=row["FG3_PCT"],
                ftm=row["FTM"],
                fta=row["FTA"],
                ft_pct=row["FT_PCT"],
                oreb=row["OREB"],
                dreb=row["DREB"],
                reb=row["REB"],
                ast=row["AST"],
                tov=row["TOV"],
                stl=row["STL"],
                blk=row["BLK"],
                blka=row["BLKA"],
                pf=row["PF"],
                pfd=row["PFD"],
                pts=row["PTS"],
                plus_minus=row["PLUS_MINUS"],
                e_off_rating=row["E_OFF_RATING"],
                off_rating=row["OFF_RATING"],
                sp_work_off_rating=row["sp_work_OFF_RATING"],
                e_def_rating=row["E_DEF_RATING"],
                def_rating=row["DEF_RATING"],
                sp_work_def_rating=row["sp_work_DEF_RATING"],
                e_net_rating=row["E_NET_RATING"],
                net_rating=row["NET_RATING"],
                sp_work_net_rating=row["sp_work_NET_RATING"],
                ast_pct=row["AST_PCT"],
                ast_to=row["AST_TO"],
                ast_ratio=row["AST_RATIO"],
                oreb_pct=row["OREB_PCT"],
                dreb_pct=row["DREB_PCT"],
                reb_pct=row["REB_PCT"],
                tm_tov_pct=row["TM_TOV_PCT"],
                e_tov_pct=row["E_TOV_PCT"],
                efg_pct=row["EFG_PCT"],
                ts_pct=row["TS_PCT"],
                usg_pct=row["USG_PCT"],
                e_usg_pct=row["E_USG_PCT"],
                e_pace=row["E_PACE"],
                pace=row["PACE"],
                pace_per40=row["PACE_PER40"],
                sp_work_pace=row["sp_work_PACE"],
                pie=row["PIE"],
                poss=row["POSS"],
            )
            for _, row in tqdm(combined_df.iterrows())
        ]

        # Use a transaction to ensure atomicity and performance
        with transaction.atomic():
            RawGameLog.objects.bulk_create(gamelog_objs, batch_size=1000)


def validate_gamelog_json(traditional, advanced) -> bool:

    if traditional["resource"] != "gamelogs" or advanced["resource"] != "gamelogs":
        log.error("'resource' field should say 'gamelogs'. json validation failed.")
        return False

    if len(traditional["resultSets"][0]["rowSet"]) != len(
        advanced["resultSets"][0]["rowSet"]
    ):
        log.error(
            "Traditional & advanced box stats have different number of entries. json validation failed."
        )
        return False

    return True


def handle_schedule(schedule_json):
    season_year = schedule_json['leagueSchedule']['seasonYear']
    game_dates = schedule_json['leagueSchedule']['gameDates']

    games = []
    for game_date in game_dates:
        for game in game_date['games']:
            games.append(game)

    schedule_objs = [
        Game(
            season_year=season_year,
            week_number=game['weekNumber'],
            game_date=game['gameDateEst'],
            home_team=game['homeTeam']['teamTricode'],
            home_team_id=game['homeTeam']['teamId'],
            away_team=game['awayTeam']['teamTricode'],
            away_team_id=game['awayTeam']['teamId'],
        )
        for game in tqdm(games)
    ]

    with transaction.atomic():
        Game.objects.bulk_create(schedule_objs, batch_size=1000)

def handle_fantasy_projections(nine_cat_list):

    fantasy_projection_objs = [
        FantasyProjection(
            season_year=row['season_year'],
            player_id=row['player_id'],
            min=row['min'],
            pts=row['pts'],
            fg3m=row['fg3m'],
            reb=row['reb'],
            ast=row['ast'],
            stl=row['stl'],
            blk=row['blk'],
            fgm=row['fgm'],
            fga=row['fga'],
            ftm=row['ftm'],
            fta=row['fta'],
            tov=row['tov'],
            usg_pct=row['usg_pct'],
        )
        for row in tqdm(nine_cat_list) if row is not None
    ]

    with transaction.atomic():
        FantasyProjection.objects.bulk_create(fantasy_projection_objs, batch_size=1000)


def handle_projection_values(season_year: str):
    league_avg = {}
    projections_df = pd.DataFrame.from_records(
        FantasyProjection.objects.filter(season_year=season_year).values()
    )

    projections_df['pts_val'] = (projections_df['pts'] - league_avg.avg_pts) / league_avg.std_pts
    projections_df['fg3m_val'] = (projections_df['fg3m'] - league_avg.avg_fg3m) / league_avg.std_fg3m
    projections_df['reb_val'] = (projections_df['reb'] - league_avg.avg_reb) / league_avg.std_reb
    projections_df['ast_val'] = (projections_df['ast'] - league_avg.avg_ast) / league_avg.std_ast
    projections_df['stl_val'] = (projections_df['stl'] - league_avg.avg_stl) / league_avg.std_stl
    projections_df['blk_val'] = (projections_df['blk'] - league_avg.avg_blk) / league_avg.std_blk
    projections_df['fg_pct_val'] = projections_df.apply(fg_val_func, league_avg=league_avg, axis=1)
    projections_df['ft_pct_val'] = projections_df.apply(ft_val_func, league_avg=league_avg, axis=1)
    projections_df['tov_val'] = 0 - (projections_df['tov'] - league_avg.avg_tov) / league_avg.std_tov
    projections_df['total_val'] = (
            projections_df['pts_val']
            + projections_df['fg3m_val']
            + projections_df['reb_val']
            + projections_df['ast_val']
            + projections_df['stl_val']
            + projections_df['blk_val']
            + projections_df['fg_pct_val']
            + projections_df['ft_pct_val']
            + projections_df['tov_val']
    )

    projection_val_objs = [
        ProjectionValue(
            season_year=row['season_year'],
            player_id=RawPlayer.objects.get(person_id=row['player_id']),
            pts_val=row['pts_val'],
            fg3m_val=row['fg3m_val'],
            reb_val=row['reb_val'],
            ast_val=row['ast_val'],
            stl_val=row['stl_val'],
            blk_val=row['blk_val'],
            fg_pct_val=row['fg_pct_val'],
            ft_pct_val=row['ft_pct_val'],
            tov_val=row['tov_val'],
            total_val=row['total_val'],
            projection_accuracy=0
        )
        for _, row in tqdm(projections_df.iterrows())
    ]

    with transaction.atomic():
        ProjectionValue.objects.bulk_create(projection_val_objs, batch_size=1000)


def fg_val_func(row, league_avg):
    raw_val = (max(0, row['fgm']) / row['fga'] - league_avg.avg_fg_pct)
    multiplier = (row['fga'] - league_avg.avg_fga) / league_avg.std_fga * 7
    if multiplier > 0:
        return raw_val * (1 + multiplier)
    else:
        return raw_val / (1 + abs(multiplier))


def ft_val_func(row, league_avg):
    ft_pct = row['ftm'] / row['fta']
    ft_pct = min(max(0, ft_pct), 1)
    raw_val = ft_pct - league_avg.avg_ft_pct
    multiplier = (row['fta'] - league_avg.avg_fta) / league_avg.std_fta * 7
    if multiplier > 0:
        return raw_val * (1 + multiplier)
    else:
        return raw_val / (1 + abs(multiplier))
