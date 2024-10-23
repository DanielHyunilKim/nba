from games.models import RawGameLog
import numpy as np
from sklearn.svm import SVR
from sklearn import preprocessing


def simple_regression(player_id, season):
    games = RawGameLog.objects.filter(player_id=player_id, season_year__lt=season)
    if len(games) > 30: # Reasonable games played cutoff
        games_df = get_9_cat(games).sort_values(by=['game_date']).reset_index()

        X = games_df.index.to_numpy().reshape((-1, 1))
        x_scaler = preprocessing.StandardScaler().fit(X)
        X_scaled = x_scaler.transform(X)

        svr = SVR(kernel='rbf', C=1, gamma=0.3)
        test_game = [X_scaled[-1] + (X_scaled[-1] - X_scaled[-2])]
        projections_9cat = {'player_id': player_id, 'season_year': season}
        youth_multiplier = max(min(4, 320 / len(X)), 1)

        for cat in ['min', 'pts', 'fg3m', 'reb', 'ast', 'stl', 'blk', 'fgm', 'fga', 'ftm', 'fta', 'tov', 'usg_pct']:
            y = games_df[cat].to_numpy()
            if cat in ['stl', 'blk']:
                y = y + 10
            svr.fit(X_scaled, y)
            projection = svr.predict(test_game)
            if cat in ['stl', 'blk']:
                projection = projection - 10
            if 75 < len(X) < 500 and youth_multiplier > 1:
                past_75_avg = np.average(y[-75:])
                if (projection - past_75_avg) > 0 and past_75_avg != 0 and cat != 'tov':
                    projection = past_75_avg * (1 + ((projection - past_75_avg) * youth_multiplier) / past_75_avg)
            projections_9cat[cat] = projection

        return projections_9cat

