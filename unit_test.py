import Goban 
import myPlayer
import time
from io import StringIO
import sys
import json

b = Goban.Board()

players = []
player1 = myPlayer.myPlayer()
player1.newGame(Goban.Board._BLACK)
players.append(player1)

player2 = myPlayer.myPlayer()
player2.newGame(Goban.Board._WHITE)
players.append(player2)

# b.push(0)
# b.push(1)
# b.push(2)
#for i in range(15):ssss
#  b.push(i-1)
#b.prettyPrint()
moves = b.legal_moves()
move = b.play_first_moves(moves)
b.push(move)
moves = b.legal_moves()
move = b.play_first_moves(moves)
b.push(move)
moves = b.legal_moves()
move = b.play_first_moves(moves)
b.push(move)
# print(Goban.Board.name_to_flat("A1"))
# b.push(Goban.Board.name_to_flat("A1"))
b.prettyPrint()
# print("Number of moves: " + str(b.get_nbMoves()))