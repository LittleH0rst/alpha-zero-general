'''
Author: Jonas Jakob
Date: May 31, 2023

Changes: JJ, June 19, 2023

Changes: JJ, June 22, 2023

Changes: JJ, June 26, 2023 - Logic for init and moves
Changes: JJ, June 27, 2023 - All Moves, Valid Moves, New board logic

Changes: JJ, July 05th, changes to board properties, logic for legal moves on current board

Changes: JJ, July 07th, logic for legal moves, finished game logic for phase 0

Changes: JJ, July 08th, logic for legal moves, phases 1 and 2, adaption for mill check function
'''
import numpy as np

class Board():
    
    """
    A Ninemensmorris Board is represented as a array of (25)
    The item on board[24] represents the placing phase. "0" if
    the phase is not over yet, "1" if it is.
    
    Board logic:
    
    The pieces are represented as
    - 1 for player one (black), 1 for player 2 (white) and 0 if there is no 
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
        self.remaining = (9,9)
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
        
        if player == -1:
            player = 0
        if remaining[player] >= 1: 
            return 0
        elif count_player_pieces(self, player) <= 3:
            return 2
        else:
            return 1
    
    """
    looks at the board, given the current player and returns the 
    locations of the players pieces in a list. 
    """
    def get_player_pieces(self, player):
        
        locations = []
        
        index = 0
        while index < len(self.pieces):
            if self.pieces[index] == player:
                locations.append(index)
            index += 1
            
        return list(locations)    
        
    """
    looks at the board and returns the indices for all empty
    positions in a list.
    """
    def get_empty_positions(self):
        
        locations = []
        
        index = 0
        while index < len(self.pieces):
            if self.pieces[index] == 0:
                locations.append(index)
            index += 1
            
        return list(locations)
    
    """
    identifies possible mills, checking if any of the moves on the current board would
    form a mill (results in a different marking for the list of all moves)
    """
    def get_possible_mills(self, move_locations, player):
        
        move_forms_mill = []
        
        for move in move_locations:
            if move != None:
                if move % 2 == 0: #move is in a corner
                    if move % 8 == 0: # move is in the top left corner of a ring
                        if (self.pieces[move + 7] == player and self.pieces[move + 6] == player): #check down
                            move_forms_mill.append(move)
                        if (self.pieces[move + 1] == player and self.pieces[move + 2] == player): #check right
                            move_forms_mill.append(move)
                    elif move in [6,14,22]: #move is in the bottom left corner of a ring
                        if (self.pieces[move + 1] == player and self.pieces[move - 6] == player): #check up
                            move_forms_mill.append(move)
                        if (self.pieces[move - 1] == player and self.pieces[move - 2] == player): #check right
                            move_forms_mill.append(move)
                    else: #move is in the bottom or top right corner of a ring
                        if (self.pieces[move + 1] == player and self.pieces[move + 2] == player): #check down/ left
                            move_forms_mill.append(move)
                        if (self.pieces[move - 1] == player and self.pieces[move - 2] == player): #check left/ up
                            move_forms_mill.append(move)
                
                else: #move is in the middle of a row
                    if move in [1,3,5,7]: #outer ring
                        if move == 7:
                            if (self.pieces[move - 7] == player and self.pieces[move - 1] == player): #check ring
                                move_forms_mill.append(move)
                        else:
                            if (self.pieces[move - 1] == player and self.pieces[move + 1] == player): #check ring
                                move_forms_mill.append(move)
                        if (self.pieces[move + 8] == player and self.pieces[move + 16] == player): #check intersections
                                move_forms_mill.append(move)
                                
                    elif move in [9,11,13,15]: #middle ring
                        if move == 15:
                            if (self.pieces[move - 7] == player and self.pieces[move - 1] == player): #check ring
                                move_forms_mill.append(move)
                        else: 
                            if (self.pieces[move - 1] == player and self.pieces[move + 1] == player): #check ring
                                move_forms_mill.append(move)
                        if (self.pieces[move + 8] == player and self.pieces[move - 8] == player): #check intersections
                                move_forms_mill.append(move)
                       
                    elif move in [17,19,21,23]: #inner ring
                        if move == 23:
                            if (self.pieces[move - 7] == player and self.pieces[move - 1] == player): #check ring
                                move_forms_mill.append(move)
                        else: 
                            if (self.pieces[move - 1] == player and self.pieces[move + 1] == player): #check ring
                                move_forms_mill.append(move)
                        if (self.pieces[move - 8] == player and self.pieces[move - 16] == player): #check intersections
                                move_forms_mill.append(move)
                
        return list(move_forms_mill)
    
    
    def check_for_mills(self, player):
        
        current_mills = []
        
        index = 0
        
        while index < 23: #check rings
            if (self.pieces[index] == self.pieces[index + 1] == self.pieces[index + 2] == player):
                current_mills.append((index, index + 1, index + 2))    
            
            index += 2
        
        index = 1
        
        while index < 8: #check intersections
            if (self.pieces[index] == self.pieces[index + 8] == self.pieces[index + 16] == player):
                current_mills.append((index, index + 8, index + 16))
            
            index += 2
            
        return list(current_mills)
    
    """
    Looks at the board, given the current player and returns a list
    with the locations of all pieces outside mills for the current 
    player
    """
    def get_pieces_outside_mills(self, player):
        
        all_pieces = get_player_pieces(self, player)
        
        mills = check_for_mills(self, player)
        
        remaining_pieces = get_player_pieces(self, player)
        
        for piece in all_pieces:
            if len(mills) != 0:
                for mill in mills:
                    if piece in mill:
                        remaining_pieces.remove(piece)
                        
                
        return list(remaining_pieces)
    
    """
    Looks at the board, given the current player and identifies all
    legal moves for the current gamestate, given that the player is
    in Phase 0
    """
    def get_legal_moves_0(self, player):
        
        #get player pieces TODO, CHECK FOR MILLS, IF ONLY MILLS, RETURN ALL
        enemies_outside_mills = get_pieces_outside_mills(self, -player)
        if len(enemies_outside_mills) > 0:
            enemies_to_take = enemies_outside_mills
        else:
            enemies_to_take = get_player_pieces(self, -player)
        
        
        #get empty positions
        empty_locations = get_empty_positions(self)
        
        #get moves -> for each move_location, check if a mill is formed (check row(s))
        mill_moves = get_possible_mills(self, empty_locations, player)
                        
        
        #generate action tuples
        moves = []
        
        for move in empty_locations:
            if move in mill_moves
                for enemy in enemies_to_take:
                    moves.append('none',move,enemy)
            else:
                moves.append('none',move,'none')
            
        
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
    
    
    
    
    
    
    
    
    
    
    
    
    
