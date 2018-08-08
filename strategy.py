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

def change_random_tiles(row_count, col_count, board, amount=4, replace="8", strategy="no_sides"):
    """
    HACK: Choose 4 random tiles not at the sides or corners.
    HACK: Currently only replacing with 8
    """
    for i in range(amount):
        if strategy == "no_sides":
            tile_loc = [randint(2, row_count-1), randint(2, col_count-1)]
            board = rep.change_tile(tile_loc, replace, board)
            rep.print_board(board)
        else:
            tile_loc = [randint(1, row_count), randint(1, col_count)]
            board = rep.change_tile(tile_loc, replace, board)
            rep.print_board(board)
    return board

#Get indexes for every numbered tile:

#for index in [range(row_count), range(col_count)]:
#for i in [col for col,x in enumerate(testlist) if x.isdigit()]:


# OPTIMIZE by skipping numbers already known.



def change_tiles_around_tile(tile_loc, condition, change, board, condition_type = None):
    around_tile = get_tiles_around_tile(tile_loc, board)
    
    for tile_info in around_tile:
        if tile_info[2][:len(condition)] == condition and condition_type == "starting_with":
            board = rep.change_tile(tile_info[:2], change, board)
        elif tile_info[2] == condition:
            board = rep.change_tile(tile_info[:2], change, board)
    
    return board

# STRATEGY Functions

def probability_nearby(board):
    """
    Merged pure logic based filling unknown tiles with flags if equal to number
    and if not equal, calculate probability
    """
    #For every numbered tile:
    numbered_tiles = get_numbered_tiles(board)
    
    for numbered_tile in numbered_tiles:
    #   Check all nearby tiles
        tile_loc = numbered_tile[:2]
        number = numbered_tile[2]
        around_tile = get_tiles_around_tile(tile_loc, board)
    
    #   Go through every unknown tile and count them
        unknown_count = 0
        for tile in around_tile:
            if tile[2][0][0] == "?":
                unknown_count += 1
            elif tile[2] == "F":
                number -= 1

    #   if number of unknown tiles == number of tile - flagged tiles:
    #       flag those unknown tiles
        if unknown_count == number:
            board = change_tiles_around_tile(tile_loc, ["?"], "F", board, condition_type = "starting_with")
        else:
            # Get probability, assign to background info of tile
            # (Make rep function to add info, but in print only give first lettter)
            # [?-0.45-0.54-0.67] for example, second or third significant digit.
            probability = round(number / unknown_count, 3)
            for tile in around_tile:
                if tile[2][0][0] == "?":
                    board = rep.change_tile(tile[:2], tile[2][:] + "-" + str(probability), board)
        
        # Scan through every tile. If[2][0] first two letters "?-", split by "-",
        # sum list and divide by len, round to 3
        for i in range(1, len(board)-1):
            for k in range(1, len(board[0])-1):
                temp_tile = rep.get_tile([i,k], board)
                if temp_tile[:2] == "?-":
                    prob_values = temp_tile.split("-")[1:]
                    total_probability = round(sum([float(x) for x in prob_values]) 
                                                    / len(prob_values), 3)
                    if total_probability > 1.0:
                        print("Probability of tile", i, k, "not possible.")
                        rep.print_board(board)
                        raise Exception
                    
                    rep.change_tile([i,k], "?-" + str(total_probability), board)
    return board


def probability_not_nearby(total_bomb_count, board):
    """
    """
    remaining_bomb_count = total_bomb_count
    not_nearby_tiles = []
    for i in range(1, len(board)-1):
        for k in range(1, len(board[0])-1):
            tile = rep.get_tile([i,k], board)
            
            if tile == "F":
                remaining_bomb_count -= 1
            elif tile[0] == "?":
                around_tile = get_tiles_around_tile([i,k], board)
                #[s for s in mylist if s.isdigit()]
                if len([temp_tile[2] for temp_tile in around_tile if temp_tile[2].isdigit()]) == 0:
                    not_nearby_tiles.append([i,k, tile])
                
    probability = round(remaining_bomb_count / len(not_nearby_tiles), 3)
    
    for tile in not_nearby_tiles:
        board = rep.change_tile(tile[:2], tile[2] + "-" + str(probability), board)
        
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
substracting that from the number of remaining bombs. We divide our resulting
number by the quantity of not-nearby tiles. This gives us the probability that
one of the not-nearby tiles is a bomb.

We then compare the lowest probability nearby tile with the not-nearby tiles'
probability.
If individual tile, choose that.
If not-nearby or equal, choose random tile which is not near walls.
"""
