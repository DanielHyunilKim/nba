from games.models import FantasyTeam, FantasyPlayer, Game
from django.db.models import Q


def get_game_counts(fantasy_team: FantasyTeam, week_number):
    fantasy_players = fantasy_team.related_players

    game_counts = {}
    for player in fantasy_players.all():
        player_name = player.__str__()
        player_team_id = player.player.team_id
        if player.injured:
            game_counts[player_name] = 0
        else:
            player_games = (Game.objects.filter(week_number=week_number)
                            .filter(Q(home_team_id=player_team_id) | Q(away_team_id=player_team_id)))
            game_counts[player_name] = len(player_games)


    return game_counts
