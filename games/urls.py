from django.urls import path

from . import views

urlpatterns = [
    # ex: /games/projections
    path("", views.projections, name="projections"),
]
