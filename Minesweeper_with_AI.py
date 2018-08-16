#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 00:09:14 2018

@author: denizhan
"""

# Formalized Strategy


"""
TODO

At the start of every strategy, the prob board is to be updated by the new board.

For every change the AI makes, the prob board is to be updated by the new board.

Or perhaps scrap that. Each time a probability change is made, we can
update it? But what about before making the probability assessment? That
won't be affected because the strategy will be utlizing the get_board function
anyway.

"""

from random import randint
from Minesweeper import Minesweeper


#Get indexes for every numbered tile:

#for index in [range(row_count), range(col_count)]:
#for i in [col for col,x in enumerate(testlist) if x.isdigit()]:


# OPTIMIZE by skipping numbers already known.

class Minesweeper_with_AI(Minesweeper):
    """
    AI to use strategies to ensure maximum probability of success.
    """

    prob_board = []


    def __init__(self, row_count=8, col_count=8, activity_mode = "game",
                 total_bomb_count=10, bomb_locations=[]):
        
        Minesweeper.__init__(self, row_count, col_count, activity_mode,
                             total_bomb_count, bomb_locations)

        self.make_prob_board()
        
        
    def make_prob_board(self):
        self.prob_board.append(["E"] * (self.col_count + 2))
        for i in range(self.row_count):
            """
            Initialize base prob_board
            """
            self.prob_board.append(["E"])
            for k in range(self.col_count):
                self.prob_board[i+1].append(["?", 0, 0.0])
            self.prob_board[i+1].append(["E", 1, 0.0])
        
        self.prob_board.append(["E", 1, 0.0] * (self.col_count + 2))


    def update_prob_board(self):
        """
        Constructs board according to row and col count.
        The main source however is the board itself (we get by get_board)
        
        Also change tiles with prob 1.0 and 0.0 .
        
        Format: [[[tile, prob], [tile, prob], ...], 
                 [[tile, prob], [tile, prob], ...]]
        
        This includes even the probabilties of empty and flagged tiles.
        """
        
        for i in range(1, self.row_count+1):
            for k in range(1, self.col_count+1):
                # format: [tile, num_of_probs, prob1, prob2, ... probN]
                tile = self.get_tile([i,k])
                if tile == "E":
                    self.prob_board[i][k] = ["E", 1, 0.0]
                elif tile.isdigit():
                    self.prob_board[i][k] = [tile, 1, 0.0]
                elif tile == "F":
                    self.prob_board[i][k] = ["F", 1, 1.0]
                
                if self.prob_board[i][k][2] == 0.0:
                    self.change_tile([i,k], "O")
                elif self.prob_board[i][k][2] == 1.0:
                    self.change_tile([i,k], "F")
                        
    
    def get_tile_and_prob(self, loc):
        """
        Returns tile and prob as [tile, prob]
        """
        return self.prob_board[loc[0]][loc[1]]
                        
        
    def change_tile_prob(self, loc, probability):
        """
        Add given probability to the tile
        Get the average by:
            the number of probabilities (self.get_tile_prob([1])
            the probabilities (self.get_tile_prob)
        """
        
        self.update_prob_board()
        
        old_avg_prob = self.prob_board[loc[0]][loc[1]][2]
        
#        assert old_avg_prob != 1.0, "You should probably not change a tile with 1.0 bomb prob"
#        
#        assert old_avg_prob != 0.0, "You should probably not change a tile with 0.0 bomb prob"
        
        self.prob_board[loc[0]][loc[1]][1] += 1
        
        # Get the second item of the tile, which indicates the number
        # of probabilities within a single tile.
        # Calculate the average probability of a single tile.
        number_of_probs = self.prob_board[loc[0]][loc[1]][1]
        prob_sum = old_avg_prob + probability
#        total_probability = round(sum([float(x) for x in prob_values]) /
#                                  number_of_probs, 1)
        avg_prob = round(prob_sum / number_of_probs)
        
        self.print_prob_board()
        
        assert 0.0 <= avg_prob <= 1.0, "Probability of tile" + str([loc[0], loc[1]]) + " with " + str(avg_prob) + "not possible."
            
        self.prob_board[loc[0]][loc[1]][2] = avg_prob
        
        self.update_prob_board()
            
    
        
#        if len(self.prob_board[loc[0]][loc[1]]) == 1:
#            self.prob_board[loc[0]][loc[1]] = [self.get_tile([loc[0], loc[1]]), probability]
#        
#        else:
#            self.prob_board[loc[0]][loc[1]] = [self.get_tile([loc[0], loc[1]]), probability]
            
        
    #def get_prob_board(self):
        

    def print_prob_board(self):
        """
        Print board as so: [[tile, prob], [tile, prob], ...]
        """
        self.update_prob_board()
        
        for i in range(1, self.row_count+1):
            for k in range(1, self.row_count+1):
                print(self.get_tile_and_prob([i,k]), end=" ")
            print()
        print()
#                tile = self.get_tile([i,k])
#                print(tile, end='')
#                if len(tile) == 1:
#                     print("------", end='')
#                print(" ", end='')
#            print()
#        print()


    def change_tiles_around_tile(self, tile_loc, condition, change):
        around_tile = self.get_tiles_around_tile(tile_loc)

        for tile_info in around_tile:
            if tile_info[2] == condition:
                self.change_tile(tile_info[:2], change)
                

#    def change_to_average_probability(self):
#        """
#        Scan through every tile. If[2][0] first two letters "?-", split by "-",
#        sum list and divide by len, round to 3
#        """
#        for i in range(1, self.row_count+1):
#            for k in range(1, self.col_count+1):
#                tile = self.get_tile_and_prob([i,k])[0]
#                tile_prob = self.get_tile_and_prob([i,k])[1]
#                if tile == "?":
#                    prob_values = temp_tile.split("-")[1:]
#                    total_probability = round(sum([float(x) for x in prob_values])
#                                                    / len(prob_values), 3)
#                    if total_probability > 1.0:
#                        print("Probability of tile", i, k, "not possible.")
#                        self.print_board()
#                        raise Exception
#                    total_probability = str(total_probability)
#                    while len(total_probability) < 5:
#                        total_probability += "0"
#
#                    self.change_tile_prob([i,k], total_probability)

    # STRATEGY Functions

    def probability_nearby(self):
        """
        Merged pure logic based filling unknown tiles with flags if equal to number
        and if not equal, calculate probability
        """

        self.prob_list = [] # [[loc, prob], [loc, prob], ...]
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
                self.change_tiles_around_tile(tile_loc, "?", "F")
                
            else:
                # Get probability, assign to background info of tile
                # (Make rep function to add info, but in print only give first lettter)
                # [?-0.45-0.54-0.67] for example, second or third significant digit.
                probability = number / unknown_count
                for tile in around_tile:
                    if tile[2][0][0] == "?":
                        self.change_tile_prob(tile[:2], probability)
                        #self.change_tile(tile[:2], tile[2][:] + "-" + str(probability))


#    def change_prob_one_zero_tiles(self):
#        
#        for i in range(1, self.row_count+1):
#            for k in range(1, self.row_count+1):
#                if self.prob_board[i][k][2] == 0.0:
#                    self.change_tile([i,k], "F")

    def probability_not_nearby(self):
        """
        """
        remaining_bomb_count = self.total_bomb_count
        not_nearby_tiles = []
        # For every non-border tile, calculate remaining bomb count and check if
        # not nearby. If not-nearby, add to list.
        for i in range(1, self.row_count+1):
            for k in range(1, self.col_count+1):
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
        probability = round(remaining_bomb_count / len(not_nearby_tiles), 1)

        # Add necessary information
        for tile in not_nearby_tiles:
            self.change_tile_prob(tile[:2], probability)



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
