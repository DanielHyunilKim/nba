import requests

from logging import getLogger

log = getLogger(__name__)


def download_game_logs(season="2023-24", date_from=None, date_to=None):
    try:
        url = "https://stats.nba.com/stats/playergamelogs"
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Host": "stats.nba.com",
            "Origin": "https://www.nba.com",
            "Referer": "https://www.nba.com/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        }
        params = {
            "DateFrom": date_from,
            "DateTo": date_to,
            "LastNGames": "0",
            "LeagueID": "00",
            "Month": "0",
            "OpponentTeamID": "0",
            "PORound": "0",
            "PaceAdjust": "N",
            "PerMode": "Totals",
            "Period": "0",
            "PlusMinus": "N",
            "Rank": "N",
            "SeasonType": "Regular Season",
            "Season": season,
        }
        traditional_params = dict(params, MeasureType="Base")
        advanced_params = dict(params, MeasureType="Advanced")

        traditional_data = requests.get(
            url=url, params=traditional_params, headers=headers, timeout=None
        )
        advanced_data = requests.get(url=url, params=advanced_params, headers=headers, timeout=None)

        return traditional_data.json(), advanced_data.json()

    except requests.exceptions.HTTPError as e:
        log.error(f"Http Error: {e}")

    except requests.exceptions.ConnectionError as e:
        log.error(f"Error Connecting: {e}")

    except requests.exceptions.Timeout as e:
        log.error(f"Timeout Error: {e}")

    except requests.exceptions.JSONDecodeError as e:
        log.error(f"JSON Error: {e}")

    except requests.exceptions.RequestException as e:
        log.error(f"Oops: Something Else {e}")


def download_players(season="2023-24", historical=1):
    try:
        url = "https://stats.nba.com/stats/playerindex"
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Host": "stats.nba.com",
            "Origin": "https://www.nba.com",
            "Referer": "https://www.nba.com/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        }
        params = {
            "Historical": historical,
            "LeagueID": "00",
            "TeamID": 0,
            "Season": season,
        }

        players = requests.get(url=url, params=params, headers=headers)
        return players.json()

    except requests.exceptions.HTTPError as e:
        log.error(f"Http Error: {e}")

    except requests.exceptions.ConnectionError as e:
        log.error(f"Error Connecting: {e}")

    except requests.exceptions.Timeout as e:
        log.error(f"Timeout Error: {e}")

    except requests.exceptions.JSONDecodeError as e:
        log.error(f"JSON Error: {e}")

    except requests.exceptions.RequestException as e:
        log.error(f"OOps: Something Else {e}")
