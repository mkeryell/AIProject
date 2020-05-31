# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

import time
import Goban
import random
import json
from random import choice
from playerInterface import *


class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None

    def getPlayerName(self):
        return "Mael"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS"
        moves = self._board.legal_moves()  # Dont use weak_legal_moves() here!
        random.shuffle(moves) #I shuffle the moves to get a somewhat more random move in the end.

        #does the opening moves according to who played "first", if there are less than 10 pieces
        nbPieces = self._board._nbBLACK + self._board._nbWHITE
        diff_pieces = self._board._nbBLACK - self._board._nbWHITE

        if (nbPieces < 10) and (abs(diff_pieces) <= 1) and ((self._board.next_player() == 1 and diff_pieces != 1) or (self._board.next_player() == 2 and diff_pieces != -1)):

            if (self._board.next_player() == 2 and diff_pieces < 1) or (self._board.next_player() == 1 and diff_pieces < 0):
                move = self.play_first_moves_inverted(moves)
            else:  
                move = self.play_first_moves(moves)
        else:
            #if there are more than 10 pieces on the board, play normally
            move = self.MaxMinABMove(moves, 2)
        assert move in moves, 'move not in legal moves'
        print("I chose the following move: " + Goban.Board.flat_to_name(move))
        self._board.push(move)

        # New here: allows to consider internal representations of moves
        print("I am playing ", self._board.move_to_str(move))
        print("My current board :")
        self._board.prettyPrint()
        # move is an internal representation. To communicate with the interface I need to change if to a string
        return Goban.Board.flat_to_name(move)

    def playOpponentMove(self, move):
        print("Opponent played ", move)  # New here
        # the board needs an internal represetation to push the move.  Not a string
        self._board.push(Goban.Board.name_to_flat(move))

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")


    def MaxMinABMove(self, moves, depth=3, alpha=None, beta=None):
        # print(len(self._empties))
        if self._board.is_game_over():
            res = self._board.result()  # White en premier, black en deuxième
            if res == "1/2-1/2":
                return 0
            if (res == "1-0" and self._board.next_player() == Goban.Board._WHITE) or (res == "0-1" and self._board.next_player() == Goban.Board._BLACK):
                return 100000
            else:
                return -100000

        if depth == 0:
            return self.evaluate()  # TODO evaluate

        move = None
        for m in moves:
            self._board.push(m)

            nm = self.MinMaxAB(depth-1, alpha, beta)
            if alpha == None or alpha < nm:
                alpha = nm
                move = m
            self._board.pop()
            if beta != None and alpha >= beta:
                return move  # beta
        return move  # , alpha

    def MaxMinAB(self, depth=3, alpha=None, beta=None):
        # print(len(self._empties))
        if self._board.is_game_over():
            res = self._board.result() #White en premier, black en deuxième
            if res == "1/2-1/2":
                return 0
            if (res == "1-0" and self._board.next_player() == Goban.Board._WHITE) or (res == "0-1" and self._board.next_player() == Goban.Board._BLACK):
                return 100000
            else:
                return -100000

        if depth == 0:
            return self.evaluate() #TODO evaluate

        
        for m in self._board.weak_legal_moves():
        # for m in self.legal_moves():
            self._board.push(m)
            nm = self.MinMaxAB(depth-1, alpha, beta)
            if alpha == None or alpha < nm:
                alpha = nm
            self._board.pop()
            if beta != None and alpha >= beta:
                return beta
        return alpha

    def MinMaxAB(self, depth=3, alpha=None, beta=None):
        # print(len(self._empties))
        if self._board.is_game_over():
            res = self._board.result()
            if res == "1/2-1/2":
                return 0
            if (res == "1-0" and self._board.next_player() == Goban.Board._BLACK) or (res == "0-1" and self._board.next_player() == Goban.Board._WHITE):
                return 100000
            else:
                return -100000

        if depth == 0:
            return (self.evaluate_opponent())

        for m in self._board.weak_legal_moves():
        # for m in self._board.legal_moves():
            self._board.push(m)
            nm = self.MaxMinAB(depth-1, alpha, beta)
            if beta == None or beta > nm:
                beta = nm
            self._board.pop()
            if alpha != None and alpha >= beta:
                return alpha
        return beta



    def evaluate_opponent(self):
        scores = self._board.compute_score()
        return scores[2 - self._board.next_player()] - scores[self._board.next_player() - 1]

        # if self.next_player == Board._BLACK:
        #     return scores[1]
        # else:
        #     return scores[0]

    def evaluate(self):
        scores = self._board.compute_score()
        return scores[self._board.next_player() - 1] - scores[2 - self._board.next_player()]

        # if self.next_player == Board._BLACK:
        #     return scores[0]
        # else:
        #     return scores[1]

    def play_first_moves(self,moves):
      with open('games.json') as json_file:
        data = json.load(json_file)
        # We first try to find a situation exactly similar. if not, we only consider the last moves, until we consider only the last move.
        nbPieces = self._board._nbBLACK + self._board._nbWHITE
        startLoop = 0
        #If the board "resets" at some point, or gets under 10 pieces, we go back to the opening moves, in which cases the white player might be playing "first"
       
        while startLoop <= nbPieces:
          for p in data:
            # we only consider games where our color won
            if (p['winner'] == "W" and self._board.next_player() == 2) or (p['winner'] == "B" and self._board.next_player() == 1):
              is_same = True
              i = startLoop
              # loop to test if the situations are the same
              while i < nbPieces and is_same:
                coord = Goban.Board.name_to_flat(p['moves'][i])
                if not self._board._board[coord] == i%2 + 1:
                  is_same = False
                i+=1
              # if we found same situation, then use move.
              if is_same and Goban.Board.name_to_flat(p['moves'][nbPieces]) in moves:
                return Goban.Board.name_to_flat(p['moves'][nbPieces])
          startLoop += 1

    def play_first_moves_inverted(self,moves):
      with open('games.json') as json_file:
        data = json.load(json_file)
        # We first try to find a situation exactly similar. if not, we only consider the last moves, until we consider only the last move.
        nbPieces = self._board._nbBLACK + self._board._nbWHITE
        startLoop = 0
        #If the board "resets" at some point, or gets under 10 pieces, we go back to the opening moves, in which cases the white player might be playing "first"
        while startLoop <= nbPieces:
          for p in data:
            # we only consider games where our color won
            if (p['winner'] == "B" and self._board.next_player() == 2) or (p['winner'] == "W" and self._board.next_player() == 1):
              is_same = True
              i = startLoop
              # loop to test if the situations are the same
              while i < nbPieces and is_same:
                coord = Goban.Board.name_to_flat(p['moves'][i])
                if not self._board._board[coord] == 2 - i%2: #inverted colors: even -> white
                  is_same = False
                i+=1
              # if we found same situation, then use move.
              if is_same and Goban.Board.name_to_flat(p['moves'][nbPieces]) in moves:
                return Goban.Board.name_to_flat(p['moves'][nbPieces])
          startLoop += 1
