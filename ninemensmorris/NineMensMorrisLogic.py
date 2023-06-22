'''
Author: Jonas Jakob
Date: May 31, 2023

Changes: JJ, June 19, 2023
'''
class Board():

    PLAYER          = [-1, 1]
    PLAYER_COLOUR   = ['Black', 'White']
    PIECES_TO_PLACE = [9, 9]
    START_STATE     = [ # number of pieces to place
                      [0, 0, 0, 0, 0, 0, 0, 0], # ring 0
                      [0, 0, 0, 0, 0, 0, 0, 0], # ring 1
                      [0, 0, 0, 0, 0, 0, 0, 0]  # ring 2
                      ]    
    MAX_MOVES_WITHOUT_MILL = 60

    def __init__(self, current_player = 1):
        "Set up initial board configuration."
        self.state          = copy.deepcopy(START_STATE)
        self.current_player = current_player
        self.selected_piece = (None, None)
        self.moved_piece    = (None, None)
        self.do_not_change  = False
        self.winner         = None
        self.pause          = True
        self.moves_without_mill      = 0
        self.savegame       = [copy.deepcopy(START_STATE)]
        self.saved          = False

  
    def countDiff(self, color):
        """Counts the # pieces of the given color
        (1 for white, -1 for black, 0 for empty spaces)"""
        
        return count

    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black
        """
        
        return list(moves)

    def has_legal_moves(self, color):
        
                        return True
        return False

    def get_moves_for_square(self, square):
        """Returns all the legal moves that use the given square as a base.
        That is, if the given square is (3,4) and it contains a black piece,
        and (3,5) and (3,6) contain white pieces, and (3,7) is empty, one
        of the returned moves is (3,7) because everything from there to (3,4)
        is flipped.
        """
        

    def execute_move(self, move, color):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color pf the piece to play (1=white,-1=black)
        """

        

    def _discover_move(self, origin, direction):
        """ Returns the endpoint for a legal move, starting at the given origin,
        moving by the given increment."""
        

    def _get_flips(self, origin, direction, color):
        """ Gets the list of flips for a vertex and direction to use with the
        execute_move function """
        

    @staticmethod
    def _increment_move(move, direction, n):
        # print(move)
        """ Generator expression for incrementing moves """
        move = list(map(sum, zip(move, direction)))
        #move = (move[0]+direction[0], move[1]+direction[1])
        while all(map(lambda x: 0 <= x < n, move)): 
        #while 0<=move[0] and move[0]<n and 0<=move[1] and move[1]<n:
            yield move
            move=list(map(sum,zip(move,direction)))
            #move = (move[0]+direction[0],move[1]+direction[1])

