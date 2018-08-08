#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 00:09:03 2018

@author: denizhan
"""

# Formalized Rules of Game

"""
CHANGE Functions.
Provides allowed core operations on board.
"""

# Notice: Mostly for Python version of game.

"""
Meaningful Symbols

? = Unknown tile.

E = Empty tile.

1, 2, 3, ... = Number of bombs around the tile.

F = Flagged tile

Shall we make the full game, or model only the rules?
Actually making the game may provide a better basis to test strategy.
Something more complex than only randomly choosing numbers instead.
"""
import representation as rep
import strategy as strat
from random import randint

#If a tile is chosen:
#change_tile()
#   If bomb:
#       Game over
#   If empty and bomb nearby:
#       Show number of tileindex
#   Else:
#       Show nearby empty tiles

def assign_bombs(total_bomb_count, bomb, tile_loc="random"):
    if tile_loc == "random":
        pass
        
        
def change_tile(tile_loc, change, board):
    """
    Function for moving on board
    
    Parameters:
        change_info is a list denoting the change desired. Format [row, col, move]
        e.g. [1,3,"F"]
        Starts from 1, 1.
    """
    board[tile_loc[0]][tile_loc[1]] = change
    #print("Play row", tile_loc[0], "col", tile_loc[1])
    return board

def change_random_tiles(row_count, col_count, board, amount=4, replace="8", strategy=""):
    """
    HACK: Choose 4 random tiles not at the sides or corners.
    HACK: Currently only replacing with 8
    """
    for i in range(amount):
        if strategy == "no_sides":
            tile_loc = [randint(2, row_count-1), randint(2, col_count-1)]
            board = change_tile(tile_loc, replace, board)
            rep.print_board(board)
        else:
            tile_loc = [randint(1, row_count), randint(1, col_count)]
            board = change_tile(tile_loc, replace, board)
            rep.print_board(board)
    return board

# Update board

