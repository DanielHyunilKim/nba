from django.contrib import admin

# from games.models import Season, Team, Player, Game, GameLog


class BaseAdmin(admin.ModelAdmin):
    list_per_page = 20
    readonly_fields = ["id"]
