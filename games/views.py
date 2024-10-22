from django.shortcuts import render
from games.models import FantasyProjection, ProjectionValue, RawGameLog
from django.core.paginator import Paginator
import pandas as pd

# Create your views here.
def projections(request):
    player_ids = [projection.player_id for projection in FantasyProjection.objects.all()]
    projections = FantasyProjection.objects.filter(season_year='2024-25')
    projection_values = ProjectionValue.objects.filter(season_year='2024-25')

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
    season_year = '2023-24'

    # league average for players playing > 15 minutes
    game_logs_qs = RawGameLog.objects.filter(season_year=season_year).values_list(
        'player_id_id', 'player_name', 'season_year', 'min', 'pts', 'fg3m', 'reb', 'ast', 'stl', 'blk', 'fgm', 'fga', 'ftm', 'fta', 'tov', 'usg_pct'
    )
    game_logs_df = pd.DataFrame(
        list(game_logs_qs),
        columns=['player_id_id', 'player_name', 'season_year', 'min', 'pts', 'fg3m', 'reb', 'ast', 'stl', 'blk', 'fgm', 'fga', 'ftm', 'fta', 'tov', 'usg_pct']
    )
    averages_df = game_logs_df.groupby(['player_id_id', 'player_name', 'season_year']).agg({
        'min': 'mean',
        'pts': 'mean',
        'fg3m': 'mean',
        'reb': 'mean',
        'ast': 'mean',
        'stl': 'mean',
        'blk': 'mean',
        'fgm': 'mean',
        'fga': 'mean',
        'ftm': 'mean',
        'fta': 'mean',
        'tov': 'mean',
        'usg_pct': 'mean',
    }).reset_index()

    league_df = averages_df[averages_df['min'] >= 15]
    averages_df['fg_pct'] = averages_df['fgm'] / averages_df['fga']
    averages_df['ft_pct'] = averages_df['ftm'] / averages_df['fta']
    league_avg_fg_pct = league_df['fgm'].sum() / league_df['fga'].sum()
    league_stddev_fg_pct = (league_df['fgm'] / league_df['fga']).std()
    league_avg_ft_pct = league_df['ftm'].sum() / league_df['fta'].sum()
    league_stddev_ft_pct = (league_df['ftm'] / league_df['fta']).std()
    league_stddev_fga = league_df['fga'].std()
    league_stddev_fta = league_df['fta'].std()

    averages_df['pts_val'] = (averages_df['pts'] - league_df['pts'].mean()) / league_df['pts'].std()
    averages_df['fg3m_val'] = (averages_df['fg3m'] - league_df['fg3m'].mean()) / league_df['fg3m'].std()
    averages_df['reb_val'] = (averages_df['reb'] - league_df['reb'].mean()) / league_df['reb'].std()
    averages_df['ast_val'] = (averages_df['ast'] - league_df['ast'].mean()) / league_df['ast'].std()
    averages_df['stl_val'] = (averages_df['stl'] - league_df['stl'].mean()) / league_df['stl'].std()
    averages_df['blk_val'] = (averages_df['blk'] - league_df['blk'].mean()) / league_df['blk'].std()
    averages_df['fg_pct_val'] = ((averages_df['fg_pct'] - league_avg_fg_pct) * averages_df['fga'] / league_stddev_fga) / league_stddev_fg_pct
    averages_df['ft_pct_val'] = ((averages_df['ft_pct'] - league_avg_ft_pct) * averages_df['fta'] / league_stddev_fta) / league_stddev_ft_pct
    averages_df['tov_val'] = 0 - (averages_df['tov'] - league_df['tov'].mean()) / league_df['tov'].std()

    averages_df['total_impact'] = averages_df['pts_val'] + averages_df['fg3m_val'] + averages_df['reb_val'] + averages_df['ast_val'] + averages_df['stl_val'] + averages_df['blk_val'] + averages_df['fg_pct_val'] + averages_df['ft_pct_val'] + averages_df['tov_val']
    averages_df = averages_df.round(decimals=2)

    player_impacts = averages_df.to_dict(orient='records')
    column_names = averages_df.columns.tolist()

    # Sorting logic for multiple fields
    sort_by = request.GET.get('sort', 'total_impact')  # Default sort by total_impact
    direction = request.GET.get('direction', 'asc')

    reverse = True if direction == 'desc' else False
    player_impacts = sorted(player_impacts, key=lambda x: x[sort_by], reverse=reverse)

    # Paginate the sorted player impacts (10 per page for example)
    paginator = Paginator(player_impacts, 10)  # Show 10 players per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'sort_by': sort_by,
        'direction': direction,
    }

    return render(request, "fantasy/index.html", context)
