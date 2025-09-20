from django.shortcuts import render
import chess.pgn
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

