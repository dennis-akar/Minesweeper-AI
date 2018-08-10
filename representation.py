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

class Board:
    """Represents the board"""
    
    # Insert constants here
    
    

def make_board(row_count=8, col_count=8):
    # Board constants
    board = []

    board.append(["E"] * (col_count + 2))
    for i in range(row_count):
        """
        Initialize base board
        """
        board.append(["E"])
        for k in range(col_count):
            board[i+1].append("?")
        board[i+1].append("E")
    
    board.append(["E"] * (col_count + 2))
    
    return board

def print_board(board):
    """
    Function to print board
    """
    for i in range(len(board)):
        for k in range(len(board[0])):
            tile = get_tile([i,k], board)
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
    return None

def get_tile(tile_loc, board):
    return board[tile_loc[0]][tile_loc[1]]

def get_numbered_tiles(board):
    numbered_tiles = [] # [[tile_row, tile_col, number], ...]
        
    for row_index, row in enumerate(board):
        for col_index, item in enumerate(row):https://github.com/
            if item.isdigit():
                numbered_tiles.append([row_index, col_index, int(item)])
    return numbered_tiles

def get_tiles_around_tile(tile_loc, board):
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
                around_tile.append([row+i, col+k, get_tile([row+i, col+k], board)])
    
    return around_tile

# Testing
    
if __name__ == "__main__":
    board = make_board()
    print_board(board)
    board = rul.change_tile([1,3], "F", board)
    print_board(board)