from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .NineMensMorrisLogic import Board
import numpy as np

class NineMensMorrisGame(Game):

    def __init__(self, n):
        self.n = n

    def getInitBoard(self):
        """
        Returns:
            startBoard: a representation of the board (ideally this is the form
                        that will be the input to your neural network)
        """
        # return initial board
        b = Board(self.n)
        return np.array(b.pieces)

    def getBoardSize(self):
        """
        Returns:
            (x,y): a tuple of board dimensions
        """
        # (a,b) tuple
        return (24, 1)

    def getActionSize(self):
        """
        Returns:
            actionSize: number of all possible actions
        
        What are all possible actions? Viewed from one player, each piece can
        be placed anywhere on the map, makes 24 actions per piece. If a mill 
        is formed, with that move, the acting player gets to remove a piece 
        from the oppenent. That makes 48 actions per piece in total.
        24*24 -> Actions in Phase 0 (24 positions to place, 23 positions to 
        take or none (+1)
        24*23*23 -> Actions in Phases 1 and 2 (24 possible origins, 23 
        positions to move to, 
        22 pieces to take  or none (+1)
        The result in total should come to 576 + 12696 = 13272
        """
        # return number of actions
        return len(b.get_all_moves())

    def getNextState(self, board, player, move):
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player

        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)
        """
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        if action == self.n*self.n:
            return (board, -player)
        b = Board(self.n)
        b.pieces = np.copy(board)
        move = (int(action/self.n), action%self.n)
        b.execute_move(move, player)
        return (b.pieces, -player)

    def getValidMoves(self, board, player):
        """
        Input:
            board: current board
            player: current player

        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board)
        legalMoves =  b.get_legal_moves(player)
        if len(legalMoves)==0:
            valids[-1]=1
            return np.array(valids)
        for x, y in legalMoves:
            valids[self.n*x+y]=1
        return np.array(valids)

    def getGameEnded(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.
               
        """
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(self.n)
        b.pieces = np.copy(board)
        if b.has_legal_moves(player):
            return 0
        if b.has_legal_moves(-player):
            return 0
        if len(b.get_player_pieces(player)) < 3:
            return -player
        if len(b.get_player_pieces(-player)) < 3:
            return player
        if b.current_moves >= b.MAX_MOVES_WITHOUT_MILL:
            return 0.1

    def getCanonicalForm(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
        """
        # return state if player==1, else return -state if player==-1
        return player*board

    def getSymmetries(self, board, pi):
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()
            
            Rotate the Board with a rotation vector, that defines the index for
            current value transformed to the rotated board.

        Returns:
            symmForms: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """
        
        
        
            
       

    def stringRepresentation(self, board):
        """
        Input:
            board: current board

        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        return board.tostring()
