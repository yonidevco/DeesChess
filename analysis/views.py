from django.shortcuts import render
from pathlib import Path
from .forms import PGNUploadForm
import chess
import chess.pgn
import io
from django.http import JsonResponse

def upload_pgn(request):
    game_info = None
    if request.method == "POST":
        form = PGNUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pgn_file = request.FILES["file"]

            text_file = io.TextIOWrapper(pgn_file.file, encoding="utf-8", errors="replace")

            game = chess.pgn.read_game(text_file)

            headers = game.headers
            result = headers.get("Result", "?")

            if result == "1-0":
                winner = headers.get("White", "White")
            elif result == "0-1":
                winner = headers.get("Black", "Black")
            else:
                winner = "Draw"

            moves = []
            board = game.board()
            for move in game.mainline_moves():
                moves.append(board.san(move))
                board.push(move)
            
            game_info = {
                "event" : headers.get("Event", "Unknown"),
                "date" : headers.get("Date", "Unknown"), 
                "white" : headers.get("White", "?"),
                "black" : headers.get("Black", "?"),
                "winner" : winner,
                "moves" : " ".join(moves),
            }
    else:
        form = PGNUploadForm()
    return render(request, "analysis/upload.html", {"form" : form, "game_info" : game_info})

board = chess.Board()

def replay_game(request):
    fen = "start"
    return render(request, 'analysis/replay.html', {'fen': fen})

def move_piece(request):
    if request.method == "POST":
        move_uci = request.POST.get("move")
        try:
            move = chess.Move.from_uci(move_uci)
            if move in board.legal_moves:
                board.push(move)
                return JsonResponse({"fen": board.fen()})
            else:
                return JsonResponse({"error": "illegal move"})
        except Exception:
            return JsonResponse({"error": "invalid move"})
    return JsonResponse({"error": "invalid request"})