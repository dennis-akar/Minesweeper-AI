#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 00:08:29 2018

@author: denizhan

!!!Why does changing board in print_board affect the global board variable?!!!

"""



from random import randint

class Minesweeper:
    """Represents the board"""
    
    # Internal Representation of Game
    
    board = []
    
    
    def __init__(self, row_count=8, col_count=8, activity_mode = "game",
                 total_bomb_count=10, bomb_locations=[]):
        """ Initializes the board"""
        self.row_count = row_count
        self.col_count = col_count
        self.activity_mode = activity_mode
        
        self.make_board()
        
        if activity_mode == "game":
            self.total_bomb_count = total_bomb_count
            self.change_random_tiles(self.total_bomb_count, "B", show_print=False)
            # Return bomb locations
            print("game")
            pass
        elif activity_mode == "analysis":
            self.bomb_locations = bomb_locations
            self.total_bomb_count = len(self.bomb_locations)
            for loc in bomb_locations:
                self.change_tile(loc, "B", show_print=False)
        elif activity_mode == "parsing":
            self.Parsing()
        print("super init accessed")
        
        
    def make_board(self):
        """ Constructs board according to row and col count"""
        self.board.append(["E"] * (self.col_count + 2))
        for i in range(self.row_count):
            """
            Initialize base board
            """
            self.board.append(["E"])
            for k in range(self.col_count):
                self.board[i+1].append("?")
            self.board[i+1].append("E")
        
        self.board.append(["E"] * (self.col_count + 2))
    
    
    def print_board(self, analysis=False):
        """ Function to print board"""
        flagged_tile_count = 0
        print("[0]", end=" ")
        for i in range(1, self.row_count+1):
            print("[" + str(i) + "]", end=" ")
        print()
        for i in range(1, self.row_count+1):
            print("[" + str(i) + "]", end="  ")
            for k in range(1, self.row_count+1):
                tile = self.get_tile([i,k], analysis)
                if tile == "F":
                    flagged_tile_count += 1
                print(tile, end='  ')
                if len(tile) == 1:
                    #print(str(i) + "," + str(k), end="")
#                    print("------", end='')
                    pass
                print(" ", end='')
            print()
        print("Flagged bombs to total bombs:", str(flagged_tile_count) + 
              "/" + str(self.total_bomb_count) + "\n")

        
    """
    GET Functions.
    Provides access of data from board.
    """
    
    def get_tile(self, tile_loc, analysis=False):
        """
        Returns tile at tile location
        Analysis=True reveals 
        """
        if analysis == True:
            try:
                return self.board[tile_loc[0]][tile_loc[1]][1]
            except IndexError:
                pass
        return self.board[tile_loc[0]][tile_loc[1]][0]
    
    def get_numbered_tiles(self):
        """
        Returns all number tiles
        TODO: Returns all number tiles observed by the player
        """
        numbered_tiles = [] # [[tile_row, tile_col, number], ...]
            
        for row_index, row in enumerate(self.board):
            for col_index, item in enumerate(row):
                if item[0].isdigit():
                    numbered_tiles.append([row_index, col_index, int(item)])
        return numbered_tiles
    
    def get_tiles_around_tile(self, tile_loc, analysis=False):
        """
        Returns [[row, col, tile_type], ...]
        """
        around_tile = []
    #   Shorten variables
        row = tile_loc[0]
        col = tile_loc[1]
        
        for i in range(-1, 2):
            for k in range(-1, 2):
                if not (i== 0 and k== 0):
                    around_tile.append([row+i, col+k, self.get_tile([row+i, col+k], analysis)])
        
        return around_tile
    
    # Formalized Rules of Game
    
    """
    CHANGE Functions.
    Provides allowed core (basic) operative functions on board.
    """
    
    def assign_bombs(self, amount=None, tile_loc=None):
        """
        Assign bombs to board, random with amount or location specific
        !!! Not sure if necessary
        """
        #if tile_loc is None:
        #    self.change_random_tiles(amount)
        pass
            
            
    def change_tile(self, tile_loc, change_to, show_print=True):
        """
        Function for moving and updating board.
        OPTIMIZE: Could have made updating a different method, perhaps later.
        
        Parameters:
            change_info is a list denoting the change desired. Format [row, col, move]
            e.g. [1,3,"F"]
            Starts from 1, 1.
        """
        # Assign bombs by making the tile into a list of "?" and "B".
        # This is so that the player cannot know whether the tile is really
        # a bomb. However, we must add a way to update the board for the
        # player, as well as check if the player opened the bomb tile (game over)
        
        if show_print:
            print("Trying to change tile at", tile_loc, "to", change_to)
        
        if change_to == "B":
            "Change to bomb"
            self.board[tile_loc[0]][tile_loc[1]] = ["?", change_to]
        
        elif change_to == "F":
            # Change to flagged
            try:
                self.board[tile_loc[0]][tile_loc[1]][0] = "F"
            except TypeError:
                self.board[tile_loc[0]][tile_loc[1]] = "F"
                
        elif change_to == "?":
            try:
                self.board[tile_loc[0]][tile_loc[1]][0] = "?"
            except TypeError:
                self.board[tile_loc[0]][tile_loc[1]] = "?"
        
        elif change_to == "O":
            # Open tile
            # If bomb, game over
            if self.get_tile(tile_loc, analysis=True) == "B":
                print("Game Over: You Lost!")
                self.print_board(analysis=True)
                return None
            # Elif not simply empty:
            elif self.get_tile(tile_loc) != "E":
            #   Check around that tile
                tiles_around_tile = self.get_tiles_around_tile(tile_loc, True)
            #   If bomb(s) around tile:
                bomb_count = 0
                for tile in tiles_around_tile:
                    if tile[2] == "B":
                        bomb_count += 1
                if bomb_count > 0:
            #       Change tile to number of bombs around tile
                    self.board[tile_loc[0]][tile_loc[1]] = str(bomb_count)
                else:
            #       Make empty
                    self.board[tile_loc[0]][tile_loc[1]] = "E"
            #       For all tiles around tile:
                    for tile in tiles_around_tile:
            #           Change tiles around tile to open as well, recursive
            #           Should not change "E"
                        self.change_tile(tile[:2], "O", show_print=False)
        
        # If probability being given           
        else:
            print("ERROR: Command not understood.")
            print("Please enter F, ? or O as a command.")
        
        if show_print:
            self.print_board()
        if self.check_if_win():
            print("Congratulations: You Won!")
    
    
    def change_random_tiles(self, amount, change_to, strategy="any tile", show_print=True):
        """
        Change random tiles on the board according to:
            amount
            change_to
            strategy (no_sides or else)
        """
        tiles_to_change_loc = []
        while len(tiles_to_change_loc) < amount:
            if strategy == "no_sides":
                tile_loc = [randint(2, self.row_count-1), randint(2, self.col_count-1)]
            else:
                tile_loc = [randint(1, self.row_count), randint(1, self.col_count)]
            
            if tile_loc not in tiles_to_change_loc:
                tiles_to_change_loc.append(tile_loc)
                    
        for tile_loc in tiles_to_change_loc:
            self.change_tile(tile_loc, change_to, show_print)
            
    def check_if_win(self):
        for i in range(1, self.row_count+1):
            for k in range(1, self.row_count+1):
                if self.get_tile([i,k]) == "?":
                    return False
        return True
    

class Parsing(Minesweeper):
    """
    Future class for parsing Minesweeper application,
    rather than Python Minesweeper.
    """
    pass
    
    

# Testing
    
if __name__ == "__main__":
    game = Minesweeper()
    game.print_board()
    print(game.get_tile([1,3]))
    print(game.get_tiles_around_tile([1,3]))
    # board = rul.change_tile([1,3], "F", board) #!!!
    #board.print_board()