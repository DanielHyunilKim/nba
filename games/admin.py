from django.contrib import admin

from games.models import RawPlayer, FantasyPlayer, FantasyTeam


class BaseAdmin(admin.ModelAdmin):
    list_per_page = 20
    readonly_fields = ["id"]


class FantasyPlayerAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "player":
            kwargs["queryset"] = RawPlayer.objects.filter(roster_status=1).order_by(
                "player_first_name", "player_last_name"
            )
        return super(FantasyPlayerAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


admin.site.register(FantasyTeam)
admin.site.register(FantasyPlayer, FantasyPlayerAdmin)
