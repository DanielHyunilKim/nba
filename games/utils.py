from games.models import FantasyTeam, WeeklyTeamGameCount


def get_game_counts(fantasy_team: FantasyTeam, week_number):
    fantasy_players = fantasy_team.related_players.select_related("player")

    team_game_counts = WeeklyTeamGameCount.objects.filter(week_number=week_number)
    team_game_counts_dict = {team.team_id: team.game_count for team in team_game_counts}

    player_game_counts = {}
    for player in fantasy_players.all():
        player_team_id = player.player.team_id
        player_game_counts[str(player)] = (
            0 if player.injured else team_game_counts_dict[player_team_id]
        )

    return player_game_counts
