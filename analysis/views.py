from django.shortcuts import render
from pathlib import Path
from .forms import PGNUploadForm
import chess.pgn
import io
import json

def uploadpgn(request):
    positions = []
    if request.method == 'POST' and request.FILES.get("pgn_file"):
        pgn_file = request.FILES["pgn_file"]
        game = chess.pgn.read_game(pgn_file)
        board = game.board()


        for move in game.mainline_moves():
            board.push(move)
            positions.append(board.fen())

    return render(request, 'analysis/index.html', {'positions': json.dumps(positions)})


def show_local_pgn(request):
    base = Path(__file__).resolve().parents[1]
    pgn_path = base/"morphy_opera.pgn"

    pgn_text = ""
    if pgn_path.exists():
        pgn_text = pgn_path.read_text(encoding="utf-8")
    else:
        pgn_text = "morphy_opera.pgn not found!"
    return render(request, "analysis/show_pgn.html", {"pgn_text" : pgn_text})

def show_game(request):
    base = Path(__file__).resolve().parents[1]
    pgn_path = base/"morphy_opera.pgn"

    with open(pgn_path, encoding="utf-8") as f:
        game = chess.pgn.read_game(f)
    
    headers = game.headers
    result = headers["Result"]

    if result == '1-0':
        winner = headers['White']
    elif result == '0-1':
        winner = headers['Black']
    else:
        winner = "Draw"
    
    moves = []
    board = game.board()

    for move in game.mainline_moves():
        moves.append(board.san(move))
        board.push(move)
        

    context = {
        "event" : headers["Event"],
        "date" : headers["Date"],
        "white" : headers["White"],
        "black" : headers["Black"],
        "winner" : winner,
        "moves" : " ".join(moves)
    }

    return render(request, "analysis/game.html", context)

def upload_pgn(request):
    game_info = None
    if request.method == "POST":
        form = PGNUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pgn_file = request.FILES["pgn_file"]

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

def replay_game(request):
    positions_json = None
    if request.method == "POST":
        form = PGNUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['pgn_file']
            text_file = io.TextIOWrapper(uploaded_file.file, encoding="utf-8", errors="replace")

            game = chess.pgn.read_game(text_file)

            board = game.board()
            positions = []
            for move in game.mainline_moves():
                positions.append(board.fen())
                board.push(move)
            positions.append(board.fen())

            positions_json = json.dumps(positions)
    else:
        form = PGNUploadForm()
    return render(request, "analysis/replay.html", {"form" : form, "positions_json" : positions_json})