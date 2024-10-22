from django.shortcuts import render
from games.models import FantasyProjection, ProjectionValue
from django.core.paginator import Paginator

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
