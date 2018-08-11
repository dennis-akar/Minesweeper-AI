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
        
        if activity_mode == "game":
            self.total_bomb_count = total_bomb_count
            self.change_random_tiles(self.total_bomb_count, "B")
            # Return bomb locations
            pass
        elif activity_mode == "analysis":
            self.bomb_
            for loc in bomb_locations:
                self.change_tile(loc, "B")
                pass
        elif activity_mode == "parsing":
            self.Parsing()
        
        self.bomb_locations = bomb_locations
        self.make_board()
        
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
    
    
    def print_board(self):
        """ Function to print board"""
        for i in range(len(self.board)):
            for k in range(len(self.board[0])):
                tile = self.get_tile([i,k])
                # Since the player shouldn't know a bomb exists, it must be concealed.
                # For now, nothing, as we are converting to class basedhttps://github.com/.
                print(tile, end='')
                if len(tile) == 1:
                    print("------", end='')
                print(" ", end='')
            print()
    #    for row in board:
    #        print((" ".join(row)))
        print()
        
    """
    GET Functions.
    Provides access of data from board.
    """
    
    def get_tile(self, tile_loc):
        """
        Returns tile at tile location
        """
        return self.board[tile_loc[0]][tile_loc[1]]
    
    def get_numbered_tiles(self):
        """
        Returns all number tiles
        TODO: Returns all number tiles observed by the player
        """
        numbered_tiles = [] # [[tile_row, tile_col, number], ...]
            
        for row_index, row in enumerate(self.board):
            for col_index, item in enumerate(row):
                if item.isdigit():
                    numbered_tiles.append([row_index, col_index, int(item)])
        return numbered_tiles
    
    def get_tiles_around_tile(self, tile_loc):
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
                    around_tile.append([row+i, col+k, self.get_tile([row+i, col+k])])
        
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
            
            
    def change_tile(self, tile_loc, change_to):
        """
        Function for moving on board.
        TODO:
            Update the board
        
        Parameters:
            change_info is a list denoting the change desired. Format [row, col, move]
            e.g. [1,3,"F"]
            Starts from 1, 1.
        """
        self.board[tile_loc[0]][tile_loc[1]] = change_to
        #print("Play row", tile_loc[0], "col", tile_loc[1])
        
    
    def change_random_tiles(self, amount, change_to, strategy="any tile"):
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
                tiles_to_change_loc.append
                    
        
        for tile_loc in tiles_to_change_loc:
            self.change_tile(tile_loc, change_to)
            self.print_board()
    

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