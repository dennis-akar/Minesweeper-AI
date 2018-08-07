#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 00:09:14 2018

@author: denizhan
"""

# Formalized Strategy
import representation as rep
from random import randint

# GET Functions

def get_numbered_tiles(board):
    numbered_tiles = [] # [[tile_row, tile_col, number], ...]
        
    for row_index, row in enumerate(board):
        for col_index, item in enumerate(row):
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
                around_tile.append([row+i, col+k, rep.get_tile([row+i, col+k], board)])
    
    return around_tile

# CHANGE Functions

def change_random_tiles(row_count, col_count, board, amount=4, strategy="no_sides"):
    """
    HACK: Choose 4 random tiles not at the sides or corners.
    HACK: Currently only replacing with 8
    """
    for i in range(amount):
        if strategy == "no_sides":
            tile_loc = [randint(2, row_count-1), randint(2, col_count-1)]
            board = rep.change_tile(tile_loc, "7", board)
            rep.print_board(board)  
    return board

#Get indexes for every numbered tile:

#for index in [range(row_count), range(col_count)]:
#for i in [col for col,x in enumerate(testlist) if x.isdigit()]:


# OPTIMIZE by skipping numbers already known.



def change_tiles_around_tile(tile_loc, condition, change, board):
    around_tile = get_tiles_around_tile(tile_loc, board)
    
    for tile_info in around_tile:
        if tile_info[2] == condition:
            board = rep.change_tile(tile_info[:2], change, board)
    
    return board

# STRATEGY Functions

def unknowns_around_equal_to_number_tile(board):
    #For every numbered tile:
    numbered_tiles = get_numbered_tiles(board)
    
    for numbered_tile in numbered_tiles:
    #   Check all nearby tiles
        tile_loc = numbered_tile[:2]
        number = numbered_tile[2]
        around_tile = get_tiles_around_tile(tile_loc, board)
    
    #   if number of unknown tiles == number of tile - flagged tiles:
    #       flag those unknown tiles
        unknown_count = 0
        for tile in around_tile:
            if tile[2] == "?":
                unknown_count += 1
            elif tile[2] == "F":
                number -= 1
        if unknown_count == number:
            board = change_tiles_around_tile(tile_loc, "?", "F", board)
    return board

def probability_nearby(board):
    numbered_tiles = get_numbered_tiles(board)
    
    for numbered_tile in numbered_tiles:
    #   Check all nearby tiles
        tile_loc = numbered_tile[:2]
        number = numbered_tile[2]
        around_tile = get_tiles_around_tile(tile_loc, board)
    
    #   Go through every unknown tile and count them
        unknown_count = 0
        tile_already_probability = []
        for tile in around_tile:
            if tile[2][0] == "?":
                unknown_count += 1
                if len(tile[2]) > 1:
                    tile_already_probability.append(tile)
            elif tile[2] == "F":
                number -= 1
        # Get probability, assign to background info of tile
        # (Make rep function to add info, but in print only give first lettter)
        # [?-0.45] for example, second or third significant digit.
        probability = number / unknown_count
        for tile in around_tile:
            if tile[2][0][0] == "?":
                board = rep.change_tile(tile[:2], tile[2][:] + "-" + str(probability), board)
        
        for i in range(1, len(board)-2):
            for k in range(1, len(board)-2):
                temp_tile = rep.get_tile([i,k], board)
                if temp_tile[:2] == "?-":
                    prob_values = temp_tile.split("-")[1:]
                    rep.change_tile([i,k], str(round(sum([float(x) for x in prob_values]) 
                                                    / len(temp_tile[1:]), 3)), board)
        
        #board = change_tiles_around_tile(tile_loc, "?", "?-" + str(probability), board)
        #for tile in tile_already_probability:
            #board = change_tile(tile[:2], (tile[2][2:] + probability) / 2, board)
    return board


"""
If we cannot find a trivial next tile, we will be using Probability Theory.

In the event that no trivial tile can be flagged or opened, we have two methods: 
for nearby unknown tiles and for remaining not-nearby unknown tiles.

Nearby method is to go through every numbered tile, count number of unknown tiles
around it, and divide the number of the numbered tile by the number of unknown tiles. 
This gives us the probability that the unknown tiles will be a bomb.

The found probability value is assigned to the unknown tiles nearby the 
numbered tile. As individual unknown tiles get different probability values 
from more than one numbered tile, an average (?perhaps a better way is available?) 
is taken for that unknown tile. The tile with the least probability is chosen.

Not-nearby method is to assess the probability that any not-nearby unknown 
tile has a bomb. This is done by calculating the minimum number of possible 
bombs nearby (worst case scenario if choosing not-nearby unknown tile) and 
substracting that from the number of non-flagged tiles. We divide our resulting
number by the quantity of not-nearby numbers. This gives us the probability that
one of the not-nearby tiles is a bomb.

We then compare the lowest probability nearby tile with the not-nearby tiles'
probability.
If individual tile, choose that.
If not-nearby or equal, choose random tile which is not near walls.
"""
