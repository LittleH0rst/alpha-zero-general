'''
Author: Jonas Jakob
Date: May 31, 2023

Changes: JJ, June 19, 2023

Changes: JJ, June 22, 2023

Changes: JJ, June 26, 2023 - Logic for init and moves
Changes: JJ, June 27, 2023 - All Moves, Valid Moves, New board logic

Changes: JJ, July 05th, changes to board properties, logic for legal moves on current board

Changes: JJ, July 07th, logic for legal moves, finished game logic for phase 0

Changes: JJ, July 08th, logic for legal moves, adaption for mill check function

Changes: JJ, July 10th, logic for legal moves, phases 1 and 2
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
    MAX_MOVES_WITHOUT_MILL = 60

    def __init__(self, current_player = 1):
        "Set up initial board configuration."
        self.pieces = np.zeros((24), dtype='int')
        self.remaining = (9,9)
        self.current_moves = 0
        
    
    def get_all_moves(self):
        
        """
        Move can be used in the same way as action.
        We need to consider different cases:
        For game Phase 0, the piece_location doesnt exist,
        because a new piece is placed on the board.
        If one of the items in the action tuple doesnt exist
        for a action, we put a string "none".
        
        """
        moves = get_all_moves_phase_zero(self) + get_all_moves_phase_one_and_two(self)
        
        
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
    def get_legal_moves(self, player):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black)
        """
        game_phase = get_game_phase(self, player)
       
        if game_phase == 0:
            return list(get_legal_moves_0(self, player))
            
        elif game_phase == 1:
            return list(get_legal_moves_1(self, player))
        elif game_phase == 2:
            return list(get_legal_moves_2(self, player))
    
    """
    Looks at the board, given the current player and identifies the
    phase of the game for the player.
    """
    def get_game_phase(self, player):
        
        current_player = player
        if player == -1:
            current_player = 0
        if remaining[current_player] >= 1: 
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
    move_locations => Array of Tuples (origin, move) 
    Each check makes sure, that the origin of the move, isnt one of the pieces in the
    potentially new mill
    """
    def get_possible_mills(self, move_locations, player):
        
        move_forms_mill = []
        
        for move in move_locations:
            if move != None:
                if move[1] % 2 == 0: #move is in a corner
                    if move[1] % 8 == 0: # move is in the top left corner of a ring
                        if (self.pieces[move[1] + 7] == player and self.pieces[move[1] + 6] == player and 
                           move[1] + 7 != move[0] and move[1] + 6 != move[0]): #check down
                            move_forms_mill.append(move)
                        if (self.pieces[move[1] + 1] == player and self.pieces[move[1] + 2] == player and
                           move[1] + 1 != move[0] and move[1] + 2 != move[0]): #check right
                            move_forms_mill.append(move)
                    elif move in [6,14,22]: #move is in the bottom left corner of a ring
                        if (self.pieces[move[1] + 1] == player and self.pieces[move[1] - 6] == player and 
                           move[1] + 1 != move[0] and move[1] - 6 != move[0]): #check up
                            move_forms_mill.append(move)
                        if (self.pieces[move[1] - 1] == player and self.pieces[move[1] - 2] == player and
                           move[1] - 1 != move[0] and move[1] - 2 != move[0]): #check right
                            move_forms_mill.append(move)
                    else: #move is in the bottom or top right corner of a ring
                        if (self.pieces[move[1] + 1] == player and self.pieces[move[1] + 2] == player and
                           move[1] + 1 != move[0] and move[1] + 2 != move[0]): #check down/ left
                            move_forms_mill.append(move)
                        if (self.pieces[move[1] - 1] == player and self.pieces[move[1] - 2] == player and
                           move[1] - 1 != move[0] and move[1] - 2 != move[0]): #check left/ up
                            move_forms_mill.append(move)
                
                else: #move is in the middle of a row
                    if move[1] in [1,3,5,7]: #outer ring
                        if move[1] == 7:
                            if (self.pieces[move[1] - 7] == player and self.pieces[move[1] - 1] == player and
                               move[1] - 7 != move[0] and move[1] - 1 != move[0]): #check ring
                                move_forms_mill.append(move)
                        else:
                            if (self.pieces[move[1] - 1] == player and self.pieces[move[1] + 1] == player and
                               move[1] - 1 != move[0] and move[1] + 1 != move[0]): #check ring
                                move_forms_mill.append(move)
                        if (self.pieces[move[1] + 8] == player and self.pieces[move[1] + 16] == player and
                           move[1] + 8 != move[0] and move[1] + 16 != move[0]): #check intersections
                                move_forms_mill.append(move)
                                
                    elif move[1] in [9,11,13,15]: #middle ring
                        if move[1] == 15:
                            if (self.pieces[move[1] - 7] == player and self.pieces[move[1] - 1] == player and
                               and move[1] - 7 != move[0] and move[1] - 1 != move[0]): #check ring
                                move_forms_mill.append(move)
                        else: 
                            if (self.pieces[move[1] - 1] == player and self.pieces[move[1] + 1] == player and
                               move[1] - 1 != move[0] and move[1] + 1 != move[0]): #check ring
                                move_forms_mill.append(move)
                        if (self.pieces[move[1] + 8] == player and self.pieces[move[1] - 8] == player and
                           move[1] + 8 != move[0] and move[1] - 8 != move[0]): #check intersections
                                move_forms_mill.append(move)
                       
                    elif move[1] in [17,19,21,23]: #inner ring
                        if move[1] == 23:
                            if (self.pieces[move[1] - 7] == player and self.pieces[move[1] - 1] == player and
                               move[1] - 7 != move[0] and move[1] - 1 != move[0]): #check ring
                                move_forms_mill.append(move)
                        else: 
                            if (self.pieces[move[1] - 1] == player and self.pieces[move[1] + 1] == player and
                               move[1] - 1 != move[0] and move[1] + 1 != move[0]): #check ring
                                move_forms_mill.append(move)
                        if (self.pieces[move[1] - 8] == player and self.pieces[move[1] - 16] == player and
                           move[1] - 8 != move[0] and move[1] - 16 != move[0]): #check intersections
                                move_forms_mill.append(move)
                
        return list(move_forms_mill)
    
    """
    Looks at the board and returns all current mills for a given player, in tuples of their coordinates
    IDEA: maybe not in tuples, but in a set of coordinates
    """
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
    given a position, this method returns a tuple with all the neighboring positions
    """
    def get_neighbours(self, position):
        
        if position != None:
                if position % 2 == 0: #position is in a corner
                    
                    if position % 8 == 0: # position is in the top left corner of a ring
                        return (positon + 1, position + 7)
                    
                    else: #position is in top right, or bottom corners
                        return (position - 1, position + 1)
                    
                else: #position is in a intersection
                    if position in [1,3,5,7]: #outer ring
                        if position == 7:
                            return (0, 6, 15)
                        else:
                            return (position - 1, position + 1, position + 8)
                            
                        
                    elif position in [9,11,13,15]: #middle ring
                        if position == 15:
                            return (7, 8, 14, 23)
                        else:
                            return (position - 8, position - 1, position + 1, position + 8)
                        
                    elif position in [17,19,21,23]: #outer ring
                        if position == 23:
                            return (15, 16, 22)
                        else:
                            return (position - 8, position - 1, position + 1) 
                    
        
        return
    
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
        
        #get enemy pieces that can be taken if a mill is formed
        enemies_outside_mills = get_pieces_outside_mills(self, -player)
        if len(enemies_outside_mills) > 0:
            enemies_to_take = enemies_outside_mills
        else:
            enemies_to_take = get_player_pieces(self, -player)
        
        
        #get empty positions, they represent all possible move locations for phase zero
        empty_locations []
        for position in get_empty_positions(self):
            empty_locations.append(('none',position))
        
        #get moves -> for each move_location, check if a mill is formed (check row(s))
        mill_moves = get_possible_mills(self, empty_locations, player)
                        
        
        #generate action tuples
        moves = []
        
        for move in empty_locations:
            if move in mill_moves
                for enemy in enemies_to_take:
                    moves.append('none',move[1],enemy)
            else:
                moves.append('none',move[1],'none')
            
        
        return list(moves)
    
    
    """
    Looks at the board, given the current player and identifies all
    legal moves for the current gamestate, given that the player is
    in Phase 1
    """
    def get_legal_moves_1(self, player):
        
        moves = []
        
        #get enemy pieces that can be taken if a mill is formed
        enemies_outside_mills = get_pieces_outside_mills(self, -player)
        if len(enemies_outside_mills) > 0:
            enemies_to_take = enemies_outside_mills
        else:
            enemies_to_take = get_player_pieces(self, -player)
            
        #get the current players pieces that will be moved    
        current_positions = get_player_pieces(self, player)
        
        #creating the first part of the moves
        part_moves = []
        
        for position in current_positions:
            neighbours = get_neighbours(self, position)
            index = 0
            for index < len(neighbours):
                if self.pieces[neighbours[index]] == 0:
                    part_moves.append(position, neighbours[index])
                index += 1
                
        #finding the part moves that create mills, then pairing them accordingly with enemy pieces to beat
        #get moves -> for each move_location, check if a mill is formed (check row(s))
        mill_moves = get_possible_mills(self, part_moves, player)
                
        for move in part_moves:
            if move in mill_moves
                for enemy in enemies_to_take:
                    moves.append(move[0],move[1],enemy)
            else:
                moves.append(move[0],move[1],'none')    
        
        
        
        return list(moves)
    
    
    """
    Looks at the board, given the current player and identifies all
    legal moves for the current gamestate, given that the player is
    in Phase 2
    """
    def get_legal_moves_2(self, player):
        
        moves = []
        
        #get enemy pieces that can be taken if a mill is formed
        enemies_outside_mills = get_pieces_outside_mills(self, -player)
        if len(enemies_outside_mills) > 0:
            enemies_to_take = enemies_outside_mills
        else:
            enemies_to_take = get_player_pieces(self, -player)
            
        #get the current players pieces that will be moved      
        current_positions = get_player_pieces(self, player)
        
        #creating the first part of the moves
        part_moves = []
        
        empty_locations = get_empty_positions(self)
        
        #pair the locations of current positions with all empty locations on the board
        for position in current_positions:
            for location in empty_locations:
                part_moves.append(position, location)
         
        #finding the part moves that create mills, then pairing them accordingly with enemy pieces to beat
        #get moves -> for each move_location, check if a mill is formed (check row(s))
        mill_moves = get_possible_mills(self, part_moves, player)
                
        for move in part_moves:
            if move in mill_moves
                for enemy in enemies_to_take:
                    moves.append(move[0],move[1],enemy)
            else:
                moves.append(move[0],move[1],'none')
        
        return list(moves)
    
    
    def has_legal_moves(self, player):
        
        return (len(get_legal_moves(self, player)) > 0)
    
    
    def execute_move(self, move, player):
        if get_game_phase(self, player) == 0:
            if player == 1:
                remaining[1] -= 1
            else:
                remaining[0] -= 1
        if move[0] != 'none':
            self.pieces[move[0]] = 0
        if move[2] != 'none':
            self.pieces[move[2]] = 0
            self.current_moves += 1
        self.pieces[move[1]] = player
    
