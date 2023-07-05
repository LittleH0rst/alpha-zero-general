'''
Author: Jonas Jakob
Date: May 31, 2023

Changes: JJ, June 19, 2023

Changes: JJ, June 22, 2023

Changes: JJ, June 26, 2023 - Logic for init and moves
Changes: JJ, June 27, 2023 - All Moves, Valid Moves, New board logic
'''
import numpy as np

class Board():
    
    """
    A Ninemensmorris Board is represented as a array of (25)
    The item on board[24] represents the placing phase. "0" if
    the phase is not over yet, "1" if it is.
    
    Board logic:
    
    The pieces are represented as
    1 for player one, -1 for player 2 and 0 if there is no 
    piece on the position (for the canonical Board the 
    current players pieces are always shown as 1 and the 
    opponents as -1). The initial board:
    
        board shape:
        [0,0,0,0,0,0,0,0,    -> outer ring
        0,0,0,0,0,0,0,0,     -> middle ring
        0,0,0,0,0,0,0,0]     -> inner ring
   
    
        
    Locations:
    
    Locations are given as the index in the board array.
    
    Actions:
    
    Actions are stored in a list of tuples of the form:
        action = [piece_location, move_location, remove_piece]
    """

    PLAYER          = [-1, 1]
    PLAYER_COLOUR   = ['Black', 'White']
    PIECES_TO_PLACE = [9, 9]
    START_STATE     = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]   
    MAX_MOVES_WITHOUT_MILL = 60
s
    def __init__(self, current_player = 1):
        "Set up initial board configuration."
        self.pieces = np.zeros((24), dtype='int')
        self.whiteInit = 9
        self.blackInit = 9
        self.current_moves = 0
        
    
    def get_all_moves(self, color):
        
        """
        Move can be used in the same way as action.
        We need to consider different cases:
        For game Phase 0, the piece_location doesnt exist,
        because a new piece is placed on the board.
        If one of the items in the action tuple doesnt exist
        for a action, we put a string "none".
        
        """
        
        return list(moves)
        
        
    """
    Generates all moves for phase zero. 
    Should create 576 moves. Tested on July 4th.
    """
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
    
    """
    Generates all moves for phase one and two.
    The difference, compared to phase zero, is that
    each move has a piece that is moved to another
    location. The rest remains the same.
    Should create 12696 moves (24*23*23). Tested on July 4th
    """
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

    
    
    
    """
    Input: board object, color
    
    IDEA: Generate Move Tuples from the Board state
    -> first implement Phase 0 (easier)
    
    TO IMPLEMENT
    - Find Game Phase for given color
    
    Phase 0
    - check if there is a possible mill (2 in a row, last empty)
    - flag the possible mills
    - for the possible mills, only mark the moves as legal, that take an enemy piece
    - for all other empty positions, only mark the placement as legal
    """
    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black)
        """
        
        
        
        
        
        
        
        
        return list(moves)
    
    """
    Looks at the board, given the current player and identifies the
    phase of the game for the player.
    """
    def get_game_phase(self, player):
        
        
        
        return phase
    
    """
    Looks at the board, given the current player and identifies all
    legal moves for the current gamestate, given that the player is
    in Phase 0
    """
    def get_legal_moves_0(self, color):
        
        self.
        
        
        return list(moves)
    
    
    """
    Looks at the board, given the current player and identifies all
    legal moves for the current gamestate, given that the player is
    in Phase 1
    """
    def get_legal_moves_1(self, color):
        
        return list(moves)
    
    
    """
    Looks at the board, given the current player and identifies all
    legal moves for the current gamestate, given that the player is
    in Phase 2
    """
    def get_legal_moves_2(self, color):
        
        return list(moves)
    
    
    def has_legal_moves(self, color):
        
                        return True
        return False
    
    
    
    
    
    
    
    
    
    
    
    
    
