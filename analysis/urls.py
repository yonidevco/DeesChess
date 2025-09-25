from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_local_pgn, name="show_local_pgn"),
    path('game/', views.show_game, name="show_game"),
    path('upload/', views.upload_pgn, name="upload_pgn"),
    path('replay/', views.replay_game, name="replay_game")
]
