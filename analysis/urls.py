from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_pgn, name="upload_pgn"),
    path('replay/', views.replay_game, name="replay_game"),
    path('move-piece/', views.move_piece, name='move_piece')
]
