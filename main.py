#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 12:29:53 2018

@author: Denizhan Akar

DESCRIPTION
An AI made from the principles which guarantee as much success as possible.

GAME: Minesweeper
TYPE: Perfect Information

TODO, by priority

Construct internal data representation of game
Formalize rules of game:
    ??? Make 2 modes: 
        ??? Play minesweeper on python
        Parse screen data and play
Formalize strategy to win game
    Choose starting locations anywhere other than middle
    For now choose just 4. If blank space is not found, continue pressing.
    
    Only consider empty tiles 
    
    If the number of empty tiles around warning number is equal to the 
    warning number minus bomb tiles flagged around it, they are bombs.
    
    Else: Probability

Use OpenCV to take minesweeper game data
Process data into internal data representation

Use Probability Theory to make wise choice

"""
# %% Internal Representation of Game

row_count = 8
col_count = 8

def make_board(row_count=8, col_count=8):
    # Board constants
    board = []

    board.append(["E"] * (col_count + 2))
    for i in range(row_count+2):
        """
        Initialize base board
        """
        board.append(["E"])
        for k in range(col_count):
            board[i+1].append("?")
        board[i+1].append("E")
    
    board.append(["E"] * (col_count + 2))
    
    return board

board = make_board(row_count, col_count)

def print_board(board):
    """
    Function to print board
    """
    for row in board:
        print((" ".join(row)))
    print()


def change_tile(tile_loc, change, board):
    """
    Function for moving on board
    
    Parameters:
        change_info is a list denoting the change desired. Format [row, col, move]
        e.g. [1,3,"F"]
        Starts from 1, 1.
    """
    board[tile_loc[0]][tile_loc[1]] = change
    print("Play row", tile_loc[0], "col", tile_loc[1])
    return board


# Testing

print_board(board)

board = change_tile([1,3], "F", board)

print_board(board)


#%% Formalized Rules of Game

# Notice: Mostly for Python version of game.

"""
Meaningful Symbols

? = Unknown tile.

E = Empty tile.

1, 2, 3, ... = Number of bombs around the tile.

F = Flagged tile
"""
#If a tile is chosen:
#change_tile()
#   If bomb:
#       Game over
#   If empty and bomb nearby:
#       Show number of tileindex
#   Else:
#       Show nearby empty tiles

#


# Update board



#%% Formalized Strategy
from random import randint

# HACK: Choose 4 random tiles not at the sides or corners.
for i in range(4):
    tile_loc = [randint(2, row_count-1), randint(2, col_count-1)]
    board = change_tile(tile_loc, "8", board)
    print_board(board)

#Get indexes for every numbered tile:

#for index in [range(row_count), range(col_count)]:
#for i in [col for col,x in enumerate(testlist) if x.isdigit()]:
    
def get_tile(tile_loc, board):
    return board[tile_loc[0]][tile_loc[1]]

def get_numbered_tiles(board):
    numbered_tiles = [] # [[tile_row, tile_col, number], ...]
        
    for row_index, row in enumerate(board):
        for col_index, item in enumerate(row):
            if item.isdigit():
                numbered_tiles.append([row_index, col_index, int(item)])
    return numbered_tiles

numbered_tiles = get_numbered_tiles(board)

# OPTIMIZE by skipping numbers already known.

# Function for tiles around a tile
def get_tiles_around_tile(tile_loc, board):
    around_tile = []
#   Shorten variables
    row = tile_loc[0]
    col = tile_loc[1]
    
    for i in range(-1, 2):
        for k in range(-1, 2):
            if not (i== 0 and k== 0):
                around_tile.append([row+i, col+k, get_tile([row+i, col+k], board)])
    
    return around_tile

def apply_to_tiles_around_tile(tile_loc, condition, change, board):
    around_tile = get_tiles_around_tile(tile_loc, board)
    
    for tile_info in around_tile:
        if tile_info[2] == condition:
            board = change_tile(tile_info[:2], change, board)
    
    return board

#For every numbered tile:
for numbered_tile in numbered_tiles:
#   Check all nearby tiles
    tile_loc = numbered_tile[:2]
    number = numbered_tile[2]
    around_tile = get_tiles_around_tile(tile_loc, board)
    
#    if row > 1:
#        top_middle = board[row-1][col]
#        if col > 1:
#            top_left = board[row-1][col-1]
#        if col < col_count:
#            top_right = board[row-1][col+1]
#    
#    if col > 1:
#        middle_left = board[row][col-1]
#    if col < col_count:
#        middle_right = board[row][col+1]
#    
#    if row < row_count:
#        bottom_middle= board[row+1][col]
#        if col > 1:
#            bottom_right = board[row+1][col+1]
#        if col < col_count:
#            bottom_left = board[row+1][col-1]
            
#   

#   if number of unknown tiles == number of tile - flagged tiles:
#       flag those unknown tiles
    unknown_count = 0
    for tile in around_tile:
        if tile[2] == "?":
            unknown_count += 1
        elif tile[2] == "F":
            number -= 1
        if unknown_count == number:
            board = apply_to_tiles_around_tile(tile_loc, "?", "F", board)
            break


"""
If we cannot find a trivial next tile, we will be using Probability Theory.

In the event that no trivial tile can be flagged or opened, we have two methods: 
for nearby unknown tiles and for remaining non-nearby unknown tiles.

Nearby method is to go through every numbered tile, count number of empty tiles
around it, and divide the number of the numbered tile by the number of empty tiles. 
This gives us the probability that the unknown tiles will be a bomb.

The found probability value is assigned to the unknown tiles nearby the 
numbered tile. As individual unknown tiles get different probability values 
from more than one numbered tile, an average (?perhaps a better way is available?) 
is taken for that unknown tile. The tile with the least probability is chosen.

Non-nearby method is to assess the probability that any non-nearby unknown 
tile has a bomb. This is done by calculating the minimum number of possible 
bombs nearby (worst case scenario if choosing non-nearby unknown tile) and 
substracting that from the number of non-flagged tiles. We divide our resulting
number by the quantity of non-nearby numbers. This gives us the probability that
one of the non-nearby tiles is a bomb.

We then compare the lowest probability nearby tile with the non-nearby tiles'
probability.
If individual tile, choose that.
If non-nearby or equal, choose random tile which is not near walls.
"""

"""
DEAD CODE
#   Go through one by one, clockwise
    around_tile = [board[row-1][col-1], board[row-1][col], board[row-1][col+1],
                     board[row][col-1], board[row][col+1],
                     board[row+1][col-1], board[row+1][col], board[row+1][col+1]]
"""





