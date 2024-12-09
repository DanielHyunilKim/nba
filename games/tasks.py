from games.api_services import download_game_logs, download_players, download_schedule
from games.db_services import (
    handle_game_logs,
    handle_players,
    handle_fantasy_projections,
    handle_projection_values,
    handle_schedule,
)
from games.projection_services import simple_regression
from celery import shared_task
from games.models import RawGameLog
from tqdm import tqdm
from django.db.models import Max
import datetime


from logging import getLogger

log = getLogger(__name__)


@shared_task()
def populate_raw_players_task(season="2024-25", historical=1):
    players = download_players(season, historical)
    handle_players(players)


@shared_task()
def populate_raw_game_logs_task(season="2024-25", date_from=None, date_to=None):
    traditional, advanced = download_game_logs(season, date_from, date_to)
    handle_game_logs(traditional, advanced)


@shared_task()
def populate_recent_game_logs_task(season="2024-25", date_from=None, date_to=None):
    recent_date = RawGameLog.objects.aggregate(Max("game_date"))["game_date__max"]
    formatted_recent_date = datetime.datetime.strptime(recent_date, "%Y-%m-%dT%H:%M:%S")
    date_from = (formatted_recent_date + datetime.timedelta(days=1)).strftime(
        "%m/%d/%Y"
    )

    traditional, advanced = download_game_logs(season, date_from, date_to)
    handle_game_logs(traditional, advanced)


@shared_task()
def populate_schedule(season="2024-25"):
    schedule = download_schedule(season)
    handle_schedule(schedule)


@shared_task()
def populate_fantasy_projection_task(season="2024-25"):
    # get players who played _previous_ season (assume season is past 2010)
    first = int(season[:4]) - 1
    second = int(season[-2:]) - 1
    prev_season = str(first) + "-" + str(second)
    player_ids = (
        RawGameLog.objects.filter(season_year=prev_season)
        .values_list("player_id", flat=True)
        .distinct()
    )
    nine_cat_list = [
        simple_regression(player_id, season) for player_id in tqdm(player_ids)
    ]
    handle_fantasy_projections(nine_cat_list)


@shared_task()
def populate_projection_value(season="2023-24"):
    handle_projection_values(season)


@shared_task()
def populate_play_by_play():
    game_ids = "game_id"
