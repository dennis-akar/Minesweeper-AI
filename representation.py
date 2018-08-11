#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 00:08:29 2018

@author: denizhan

!!!Why does changing board in print_board affect the global board variable?!!!

"""

# Internal Representation of Game
"""
GET Functions.
Provides access of data from board.
"""

class Minesweeper:
    """Represents the board"""
    
    board = []
    
    # Insert constants here
    
    def __init__(self, row_count=8, col_count=8, activity_mode = "game",
                 total_bomb_count=10, bomb_locations=[]):
        """ Initializes the board"""
        self.row_count = row_count
        self.col_count = col_count
        # game or analysis activity_mode
        self.activity_mode = activity_mode
        if activity_mode == "game":
            self.total_bomb_count = total_bomb_count
            # Currently not functioning
            #self.change_random_tiles(change_to=total_bomb_count)
            pass
        elif activity_mode == "analysis":
            for loc in bomb_locations:
                #self.change_tile(loc, "B")
                pass
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
    
    def get_tile(self, tile_loc):
        return self.board[tile_loc[0]][tile_loc[1]]
    
    def get_numbered_tiles(self):
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

# Testing
    
if __name__ == "__main__":
    game = Minesweeper()
    game.print_board()
    print(game.get_tile([1,3]))
    print(game.get_tiles_around_tile([1,3]))
    # board = rul.change_tile([1,3], "F", board) #!!!
    #board.print_board()