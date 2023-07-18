from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .NineMensMorrisLogic import Board
import numpy as np

class NineMensMorrisGame(Game):
    square_content = {
        -1: "B",
        +0: "-",
        +1: "W"
    }

    def __init__(self):
      self.n = 5
      self.all_moves = self.get_all_moves()
      self.policy_rotation_vector = self.get_policy_roation90()
      self.current_moves = 0
      self.MAX_MOVES_WITHOUT_MILL = 50


    def get_all_moves(self):
       moves = self.get_all_moves_phase_zero() + self.get_all_moves_phase_one_and_two()
       return list(moves)

    def get_policy_roation90(self):

        rotation90 = [-1] * len(self.all_moves)

        i = 0
        while i < len(self.all_moves):

            move = self.all_moves[i]
            rotatedmove = self.rotate(move)
            newindex = self.all_moves.index(rotatedmove)
            rotation90[i] = newindex

            i+=1

        return rotation90

    def rotate(self, move):

        if move[0] == 'none':
            neworigin = 'none'

        elif move[0] in [6,7,14,15,22,23]:
            neworigin = move[0] - 6

        else:
            neworigin = move[0] + 2

        if move[1] in [6,7,14,15,22,23]:
            newdestination = move[1] - 6

        else:
            newdestination = move[1] + 2

        if move[2] == 'none':
            newenemy = 'none'

        elif move[2] in [6,7,14,15,22,23]:
            newenemy = move[2] - 6

        else:
            newenemy = move[2] + 2

        return (neworigin, newdestination, newenemy)

    def get_all_moves_phase_zero(self):

        moves = []
        index = 0

        while index < 24:

            moves.append(("none",index,"none"))
            count = 0

            while count < 24:

                if count != index:

                    moves.append(("none",index,count))

                count += 1

            index += 1

        return list(moves)

    def get_all_moves_phase_one_and_two(self):

        moves = []
        index_origin = 0

        while index_origin < 24:

            index_move = 0

            while index_move < 24:

                if index_move != index_origin:

                    moves.append((index_origin,index_move,"none"))

                    count = 0

                    while count <24:

                        if (count != index_move)and(count != index_origin):

                            moves.append((index_origin,index_move,count))

                        count += 1

                index_move += 1

            index_origin += 1

        return list(moves)

    def getInitBoard(self):

        # return initial board
        b = Board()

        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (5, 5)

    def getActionSize(self):
        # return number of actions
        return len(self.all_moves)

    def getNextState(self, board, player, move):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        b = Board()
        b.pieces = np.copy(board)

        try:
          self.current_moves  = b.execute_move(player, move, self.all_moves, self.current_moves)
        except IndexError as e:
          print(e)
          print(player)
          print(move)

        return (b.pieces, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        b = Board()
        b.pieces = np.copy(board)
        valid_moves = b.get_legal_move_vector(player, self.all_moves)

        return np.array(valid_moves)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        if isinstance(board, str):
          b = Board()
          counter = 0
          for element in board:
            b.pieces[counter] = int(element)
            counter += 1
        else:
          b = Board()
          b.pieces = np.copy(board)
        if b.has_legal_moves(player):
            return 0
        elif not b.has_legal_moves(player):
            return -1
        if b.has_legal_moves(-player):
            return 0
        elif not b.has_legal_moves(-player):
            return 1
        if len(b.get_player_pieces(player)) < 3:
            return -1
        if len(b.get_player_pieces(-player)) < 3:
            return 1
        if b.pieces[24] >= b.MAX_MOVES_WITHOUT_MILL:
            return 0.1

    def getCanonicalForm(self, board, player):
        return player*board

    def getSymmetries(self, board, pi):

        assert(len(pi) == len(self.all_moves))
        b = Board()
        b.pieces = np.copy(board)
        results = b.get_board_rotations(board, pi, self.all_moves, self.policy_rotation_vector)

        return results

    def stringRepresentation(self, board):
        return board.tostring()

    def stringRepresentationReadable(self, board):
        board_s = "".join(self.square_content[square] for row in board for square in row)
        return board_s
