from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.postgres.fields import ArrayField


class RawPlayer(TimeStampedModel):
    person_id = models.IntegerField(primary_key=True)  # 201144
    player_last_name = models.CharField(max_length=50)  # "Conley"
    player_first_name = models.CharField(max_length=50)  # "Mike"
    player_slug = models.CharField(max_length=50)  # "mike-conley"
    team_id = models.IntegerField()  # 1610612750
    team_slug = models.CharField(max_length=50, null=True)  # "timberwolves"
    is_defunct = models.IntegerField()  # 0
    team_city = models.CharField(max_length=50)  # "Minnesota"
    team_name = models.CharField(max_length=50)  # "Timberwolves"
    team_abbreviation = models.CharField(max_length=3)  # "MIN"
    jersey_number = models.CharField(max_length=10, null=True)  # "10"
    position = models.CharField(max_length=10, null=True)  # "G"
    height = models.CharField(max_length=10, null=True)  # "6-0"
    weight = models.CharField(max_length=10, null=True)  # "175"
    college = models.CharField(max_length=50, null=True)  # "Ohio State"
    country = models.CharField(max_length=50, null=True)  # "USA"
    draft_year = models.IntegerField(null=True)  # 2007
    draft_round = models.IntegerField(null=True)  # 1
    draft_number = models.IntegerField(null=True)  # 4
    roster_status = models.IntegerField(null=True)  # 1

    def __str__(self):
        return f"{self.player_first_name} {self.player_last_name}"

    class Meta:
        ordering = ["player_first_name", "player_last_name"]


# Single game log for each player
class RawGameLog(TimeStampedModel):
    # shared
    season_year = models.CharField(max_length=10)  # "2023-24"
    player_id = models.IntegerField()  # 201144
    player_name = models.CharField(max_length=50)  # "Mike Conley"
    nickname = models.CharField(max_length=50)  # "Mike"
    team_id = models.IntegerField()  # 1610612750
    team_abbreviation = models.CharField(max_length=3)  # "MIN"
    team_name = models.CharField(max_length=50)  # "Minnesota Timberwolves"
    game_id = models.CharField(max_length=20)  # "0022301194"
    game_date = models.CharField()  # "2024-04-14T00:00:00"
    matchup = models.CharField(max_length=20)  # "MIN vs. PHX"
    wl = models.CharField(max_length=1)  # "L"
    min = models.FloatField()  # 27.433333333333334

    # traditional
    fgm = models.IntegerField()  # 5
    fga = models.IntegerField()  # 7
    fg_pct = models.FloatField()  # 0.714
    fg3m = models.IntegerField()  # 4
    fg3a = models.IntegerField()  # 5
    fg3_pct = models.FloatField()  # 0.8
    ftm = models.IntegerField()  # 3
    fta = models.IntegerField()  # 3
    ft_pct = models.FloatField()  # 1
    oreb = models.IntegerField()  # 1
    dreb = models.IntegerField()  # 3
    reb = models.IntegerField()  # 4
    ast = models.IntegerField()  # 2
    tov = models.IntegerField()  # 3
    stl = models.IntegerField()  # 1
    blk = models.IntegerField()  # 2
    blka = models.IntegerField()  # 0
    pf = models.IntegerField()  # 1
    pfd = models.IntegerField()  # 2
    pts = models.IntegerField()  # 17
    plus_minus = models.IntegerField()  # -14

    # advanced
    e_off_rating = models.FloatField()  # 104
    off_rating = models.FloatField()  # 109.6
    sp_work_off_rating = models.FloatField()  # 109.6
    e_def_rating = models.FloatField()  # 127.6
    def_rating = models.FloatField()  # 131.5
    sp_work_def_rating = models.FloatField()  # 131.5
    e_net_rating = models.FloatField()  # -23.6
    net_rating = models.FloatField()  # -21.9
    sp_work_net_rating = models.FloatField()  # -21.9
    ast_pct = models.FloatField()  # 0.154
    ast_to = models.FloatField()  # 0.67
    ast_ratio = models.FloatField()  # 15.4
    oreb_pct = models.FloatField()  # 0.053
    dreb_pct = models.FloatField()  # 0.136
    reb_pct = models.FloatField()  # 0.098
    tm_tov_pct = models.FloatField()  # 23.1
    e_tov_pct = models.FloatField()  # 22.5
    efg_pct = models.FloatField()  # 1
    ts_pct = models.FloatField()  # 1.022
    usg_pct = models.FloatField()  # 0.19
    e_usg_pct = models.FloatField()  # 0.189
    e_pace = models.FloatField()  # 96.62
    pace = models.FloatField()  # 92.73
    pace_per40 = models.FloatField()  # 77.28
    sp_work_pace = models.FloatField()  # 92.73
    pie = models.FloatField()  # 0.175
    poss = models.FloatField()  # 52

    class Meta:
        indexes = [
            models.Index(fields=["season_year", "player_id", "player_name"]),
        ]


class FantasyProjection(TimeStampedModel):
    season_year = models.CharField(max_length=10)
    player_id = models.ForeignKey(RawPlayer, on_delete=models.CASCADE)
    min = models.FloatField()
    pts = models.FloatField()
    fg3m = models.FloatField()
    reb = models.FloatField()
    ast = models.FloatField()
    stl = models.FloatField()
    blk = models.FloatField()
    fgm = models.FloatField()
    fga = models.FloatField()
    ftm = models.FloatField()
    fta = models.FloatField()
    tov = models.FloatField()
    usg_pct = models.FloatField()

    @property
    def fg_pct(self):
        return float(self.fgm) / float(self.fga) * 100

    @property
    def ft_pct(self):
        return float(self.ftm) / float(self.fta) * 100


class ProjectionValue(TimeStampedModel):
    season_year = models.CharField(max_length=10)
    player_id = models.ForeignKey(RawPlayer, on_delete=models.CASCADE)
    pts_val = models.FloatField()
    fg3m_val = models.FloatField()
    reb_val = models.FloatField()
    ast_val = models.FloatField()
    stl_val = models.FloatField()
    blk_val = models.FloatField()
    fg_pct_val = models.FloatField()
    ft_pct_val = models.FloatField()
    tov_val = models.FloatField()
    total_val = models.FloatField()
    projection_accuracy = models.FloatField()


class Game(TimeStampedModel):
    season_year = models.CharField(max_length=10)
    week_number = models.IntegerField()
    game_date = models.CharField()
    game_id = models.CharField()
    home_team = models.CharField()
    home_team_id = models.IntegerField()
    away_team = models.CharField()
    away_team_id = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=["week_number"]),
            models.Index(fields=["home_team_id", "away_team_id"]),
        ]


class WeeklyTeamGameCount(TimeStampedModel):
    season_year = models.CharField(max_length=10)
    week_number = models.IntegerField()
    team_id = models.IntegerField()
    game_count = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=["team_id"]),
        ]
        unique_together = ("season_year", "team_id", "week_number")


class FantasyTeam(TimeStampedModel):
    team_name = models.CharField(max_length=50)

    def __str__(self):
        return self.team_name

    class Meta:
        indexes = [
            models.Index(fields=["team_name"]),
        ]


class FantasyPlayer(TimeStampedModel):
    fantasy_team = models.ForeignKey(
        FantasyTeam, related_name="related_players", null=True, on_delete=models.CASCADE
    )
    player = models.ForeignKey(RawPlayer, on_delete=models.CASCADE)
    injured = models.BooleanField(default=False)

    def __str__(self):
        return str(self.player)
