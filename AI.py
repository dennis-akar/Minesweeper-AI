#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 00:09:14 2018

@author: denizhan
"""

# Formalized Strategy
"""
STRATEGY Functions.
Forms the possible strategies of the AI.
"""
#import representation as rep
#import rules as rul
from random import randint
from Minesweeper import Minesweeper


#Get indexes for every numbered tile:

#for index in [range(row_count), range(col_count)]:
#for i in [col for col,x in enumerate(testlist) if x.isdigit()]:


# OPTIMIZE by skipping numbers already known.

class AI(Minesweeper):
    """
    AI to use strategies to ensure maximum probability of success.
    """
    
    def change_tiles_around_tile(self, tile_loc, condition, change, condition_type = None):
        around_tile = self.get_tiles_around_tile(tile_loc)
        
        for tile_info in around_tile:
            if tile_info[2][:len(condition)] == condition and condition_type == "starting_with":
                self.change_tile(tile_info[:2], change)
            elif tile_info[2] == condition:
                self.change_tile(tile_info[:2], change)
    
    def change_to_average_probability(self):
        """
        Scan through every tile. If[2][0] first two letters "?-", split by "-",
        sum list and divide by len, round to 3
        """
        for i in range(1, len(self.board)-1):
            for k in range(1, len(self.board[0])-1):
                temp_tile = self.get_tile([i,k])
                if temp_tile[:2] == "?-":
                    prob_values = temp_tile.split("-")[1:]
                    total_probability = round(sum([float(x) for x in prob_values]) 
                                                    / len(prob_values), 3)
                    if total_probability > 1.0:
                        print("Probability of tile", i, k, "not possible.")
                        self.print_board()
                        raise Exception
                    total_probability = str(total_probability)
                    while len(total_probability) < 5:
                        total_probability += "0"
    
                    self.change_tile([i,k], "?-" + total_probability)
    
    # STRATEGY Functions
    
    def probability_nearby(self):
        """
        Merged pure logic based filling unknown tiles with flags if equal to number
        and if not equal, calculate probability
        """
        #For every numbered tile:
        numbered_tiles = self.get_numbered_tiles()
        
        for numbered_tile in numbered_tiles:
        #   Check all nearby tiles
            tile_loc = numbered_tile[:2]
            number = numbered_tile[2]
            around_tile = self.get_tiles_around_tile(tile_loc)
        
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
                self.change_tiles_around_tile(tile_loc, ["?"], "F", condition_type = "starting_with")
            else:
                # Get probability, assign to background info of tile
                # (Make rep function to add info, but in print only give first lettter)
                # [?-0.45-0.54-0.67] for example, second or third significant digit.
                probability = round(number / unknown_count, 3)
                for tile in around_tile:
                    if tile[2][0][0] == "?":
                        self.change_tile(tile[:2], tile[2][:] + "-" + str(probability))
            
            self.change_to_average_probability()
    
    
    def probability_not_nearby(self):
        """
        """
        remaining_bomb_count = self.total_bomb_count
        not_nearby_tiles = []
        # For every non-border tile, calculate remaining bomb count and check if
        # not nearby. If not-nearby, add to list.
        for i in range(1, len(self.board)-1):
            for k in range(1, len(self.board[0])-1):
                tile = self.get_tile([i,k])
                
                # If flagged, substract from remaining bomb count
                if tile == "F":
                    remaining_bomb_count -= 1
                
                # If unknown, check if not-nearby.
                elif tile[0] == "?":
                    around_tile = self.get_tiles_around_tile([i,k])
                    # Check if surrounding tiles are not string type integers,
                    # as that means it is not-nearby.
                    if len([temp_tile[2] for temp_tile in around_tile if temp_tile[2].isdigit()]) == 0:
                        not_nearby_tiles.append([i,k, tile])
                
                # HACK If number tile, substract 1 from remaining bomb count.
                # TODO: Find nearby number tiles, substract by combination possible
                # which would minimize nearby bomb count.
                elif tile.isdigit():
                    remaining_bomb_count -= 1
                    
        # Calculate probability
        probability = round(remaining_bomb_count / len(not_nearby_tiles), 3)
        
        # Add necessary information
        for tile in not_nearby_tiles:
            self.change_tile(tile[:2], tile[2] + "-" + str(probability))
        
        self.change_to_average_probability()



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
