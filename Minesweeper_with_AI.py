#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 00:09:14 2018

@author: Denizhan Akar

"""


from random import randint
from Minesweeper import Minesweeper


# OPTIMIZE by skipping numbers already known.

class Minesweeper_with_AI(Minesweeper):
    """
    AI to use formalized strategies to ensure maximum probability of success.
    """
    def __init__(self, row_count=8, col_count=8, activity_mode = "game",
                 total_bomb_count=10, bomb_locations=[], board=[]):
        
        Minesweeper.__init__(self, row_count, col_count, activity_mode,
                             total_bomb_count, bomb_locations, board)

        self.make_prob_board()
        
        while self.game_over_state == 0:
            print("ai_next_move")
            self.ai_next_move()
            self.simulate()
        
            
    
    def ai_next_move(self, simulation=False):
        """
        AI makes its next move.
        Makes changes to the real board according to probability.
        
        TODO
        Simulated version of AI to reflect on simulated board?
        Perhaps make copy of probability board here?
        """
        
        if not simulation:
            self.make_prob_board()
            self.update_prob_board()
        
        self.probability_nearby()
        self.probability_not_nearby()
        
        self.print_prob_board()
        
        
        least_prob = 1.0
        least_prob_locs = []
        
        for i in range(1, self.row_count+1):
            for k in range(1, self.col_count+1):
                # format: [tile, num_of_probs, prob1, prob2, ... probN]
                tile_and_prob = self.get_tile_and_prob([i,k])
                
                tile = tile_and_prob[0]
                assigned_probs_count = tile_and_prob[1]
                prob = tile_and_prob[2]
                
                if tile == "?" and assigned_probs_count > 0:
                    if prob < least_prob:
                        least_prob = prob
                        least_prob_locs = [[i,k]]
                        
                    elif prob == least_prob:
                        least_prob_locs.append([i,k])
                        
                    if prob == 1.0:
                        if not simulation:
                            self.change_tile([i,k], "F")
                            self.update_prob_board()
                        else:
                            self.change_tile_prob([i,k], 1.0, simulation)
        
        if len(least_prob_locs) == 0:
            print("No move to make! - AI")
            return None
        
        tile_to_change = least_prob_locs[0]
        
        if len(least_prob_locs) > 1:
            for loc in least_prob_locs:
                if 1 < loc[0] < self.row_count and 1 < loc[1] < self.col_count:
                    tile_to_change = [loc[0], loc[1]]
                    break
                elif 1 < loc[0] < self.row_count or 1 < loc[1] < self.col_count:
                    tile_to_change = [loc[0], loc[1]]
                else:
                    tile_to_change = [loc[0], loc[1]]
        
        if not simulation:
            self.change_tile(tile_to_change[:2], "O")
        else:
            self.change_tile_prob([i,k], 0.0, simulation)
        
        
    def make_prob_board(self):
        """
        Make probability board.
        """
        print("Making probability board...")
        self.prob_board = []
        self.prob_board.append(["E"] * (self.col_count + 2))
        for i in range(self.row_count):
            """
            Initialize base prob_board
            """
            self.prob_board.append(["E"])
            for k in range(self.col_count):
                self.prob_board[i+1].append(["?", 0, 0.0])
            self.prob_board[i+1].append(["E", 0, 0.0])
        
        self.prob_board.append(["E"] * (self.col_count + 2))



    def update_prob_board(self):
        """
        Constructs board according to row and col count.
        The main source however is the board itself (we get by get_board)
        
        Format: [[[tile, prob], [tile, prob], ...], 
                 [[tile, prob], [tile, prob], ...]]
        
        This includes even the probabilties of empty and flagged tiles.
        """
        
        print("Updating probability board...")
        
        for i in range(1, self.row_count+1):
            for k in range(1, self.col_count+1):
                # format: [tile, num_of_probs, prob1, prob2, ... probN]
                tile = self.get_tile([i,k])
                if tile == "E":
                    self.prob_board[i][k] = ["E", 0, 0.0]
                elif tile.isdigit():
                    self.prob_board[i][k] = [tile, 0, 0.0]
                elif tile == "F":
                    self.prob_board[i][k] = ["F", 0, 1.0]
                        

    
    def get_tile_and_prob(self, loc):
        """
        Returns tile and prob as [tile, prob]
        """
        return self.prob_board[loc[0]][loc[1]]
                        

        
    def change_tile_prob(self, loc, probability, simulation=False):
        """
        Try to alter probability of tile at loc.
        (Strategy defaults to minimax and cannot be modified.)
        
        If simulation=True, make direct alteration to board.
        """        
        if simulation:
            if probability == 1.0:
                self.prob_board[loc[0]][loc[1]][:2] = ["F", 0, 0.0]
            if probability == 0.0:
                self.prob_board[loc[0]][loc[1]][:2] = ["E", 0, 0.0]
            return None
        
        # Set strategy.
        strategy = "minimax" # minimax/average
        
        # Get old probability of tile.
        old_prob = self.prob_board[loc[0]][loc[1]][2]
        
#        assert old_avg_prob != 1.0, "You should probably not change a tile with 1.0 bomb prob"
#        assert old_avg_prob != 0.0, "You should probably not change a tile with 0.0 bomb prob"
        
        # Increase tile prob count
        self.prob_board[loc[0]][loc[1]][1] += 1
        
        # Get the number of times tile was assigned a probability.
        assigned_probs_count = self.prob_board[loc[0]][loc[1]][1]
        
        # If strategy is to average probabilities (DEPRECATED)        
        if strategy == "average":
            # Calculate the average probability of a single tile.
            number_of_probs = self.prob_board[loc[0]][loc[1]][1]
            prob_sum = old_prob + probability
    
            new_prob = round(prob_sum / number_of_probs, 2)
        
        # If strategy is to minimax (highest probability of bomb gets precedence)
        # with exemptions such as old tile having been purposefully assigned
        # 0.0 or 1.0 probability.
        elif strategy == "minimax":
            if old_prob == 1.0 or (old_prob == 0.0 and assigned_probs_count > 1):
                new_prob = round(old_prob, 2)
            elif probability == 1.0 or probability == 0.0:
                new_prob = round(probability, 2)
            elif probability > old_prob:
                new_prob = round(probability, 2)
            else:
                new_prob = round(old_prob, 2)
        
        # Assert that new probability is not absurd, if absurd give AssertionError.
        assert 0.0 <= new_prob <= 1.0, "Probability of tile" + str([loc[0], loc[1]]) + " with " + str(new_prob) + "not possible."
        
        # Finally replace with new probability.
        self.prob_board[loc[0]][loc[1]][2] = new_prob

        

    def print_prob_board(self):
        """
        Print probability board as so: [[tile, prob], [tile, prob], ...]
        """
        for i in range(1, self.row_count+1):
            for k in range(1, self.row_count+1):
                text = str(self.get_tile_and_prob([i,k]))
                while len(text) < 14:
                    text += " "
                print(text, end=" ")
            print()
        print()



    def change_tiles_prob_around_tile(self, tile_loc, condition, change):
        around_tile = self.get_tiles_around_tile(tile_loc)

        for tile_info in around_tile:
            if tile_info[2] == condition:
                self.change_tile_prob(tile_info[:2], change)


    # STRATEGY Functions

    def probability_nearby(self):
        """
        Merged pure logic based filling unknown tiles with flags if equal to number
        and if not equal, calculate probability.
        
        We list the digit tiles from least unknowns (min 2) to most for the
        simulation to use, no need to write the same code again.
        self.simulate() will probably be used only by probability_nearby anyway
        since it is directly related to their probabilities.
        
        The main problem with this function is that it is not consistent
        in changing the real tile:
            change tile if prob 1, which is not even given a prob
            else just give prob
            
        We need to just give it the prob for all events.
        The actual changing will be done by AI next move.
        """
        print("Calculating the probability of nearby tiles...")
        
        # List of digits with their unknowns.
        # Format: [ [[digitloc], [unknown1loc], [unknown2loc], ..., [unknownNloc]] ]
        self.digits_and_their_unknowns = []
        
        # For every numbered tile:
        numbered_tiles = self.get_numbered_tiles()

        for numbered_tile in numbered_tiles:
            # Check all nearby tiles
            tile_loc = numbered_tile[:2]
            number = numbered_tile[2]
            around_tile = self.get_tiles_around_tile(tile_loc) 

            # Go through every unknown tile and count them.
            unknown_count = 0
            
            # Make list of unknowns around number
            number_unknown_locs = [number]
            
            for tile in around_tile:
                if tile[2] == "?":
                    # Add to unknown count
                    unknown_count += 1
                    # Add to unknown loc list
                    number_unknown_locs.append(tile[:2])
                # If bomb, then already we have one
                elif tile[2] == "F":
                    number -= 1

        #   if number of unknown tiles == number of tile - flagged tiles:
        #       probablility that they are bombs is 1.0
            if unknown_count == int(number):
                self.change_tiles_prob_around_tile(tile_loc, "?", 1.0)
                
            else:
                # Get probability, assign to background info of tile
                # (Make rep function to add info, but in print only give first lettter)
                # [?-0.45-0.54-0.67] for example, second or third significant digit.
                probability = round(number / unknown_count, 3)
                print("number", number, "unknown", unknown_count, "loc", tile_loc, "nearprob", probability)
                
                self.digits_and_their_unknowns.append(number_unknown_locs)
                
                for tile in around_tile:
                    if tile[2] == "?":
                        self.change_tile_prob(tile[:2], probability)
                        
        self.digits_and_their_unknowns.sort(key=len)



    def probability_not_nearby(self):
        """
        TODO
        For every tile:
            If F, append loc to possible_bombs. Substract 1 from remaining bombs
            If digit, check around, substract from digit for every number
            Basically best case scenario for nearby probs, remove the number of
            bombs from remaining bombs
            Then give probability.
        """
        
        print("Calculating the probability of not-nearby tiles...")
        
        remaining_bomb_count = self.total_bomb_count
        not_nearby_tiles = []
        # For every non-border tile, calculate remaining bomb count and check if
        # not nearby. If not-nearby, add to list.
        
        nearby_unknown_locations = []
        
        for i in range(1, self.row_count+1):
            for k in range(1, self.col_count+1):
                tile = self.get_tile([i,k])

                # If flagged, substract from remaining bomb count
                if tile == "F":
                    remaining_bomb_count -= 1

                # If unknown, check if not-nearby.
                elif tile == "?":
                    around_tile = self.get_tiles_around_tile([i,k])
                    # Check if surrounding tiles are not string type integers,
                    # as that means it is not-nearby.
                    if len([temp_tile[2] for temp_tile in around_tile if isinstance(temp_tile[2], int)]) == 0:
                        not_nearby_tiles.append([i,k, tile])

                # HACK If number tile, substract 1 from remaining bomb count.
                # TODO: Find nearby number tiles, substract by combination possible
                # which would minimize nearby bomb count.
                
                # Get locations of nearby unknowns
                elif tile.isdigit():
                    for i_temp, k_temp, tile_type in self.get_tiles_around_tile([i,k]):
                        if tile_type == "?" and [i_temp,k_temp] not in nearby_unknown_locations:
                            nearby_unknown_locations.append([i_temp,k_temp])
                    remaining_bomb_count -= 1

        if len(not_nearby_tiles) == 0:
            return None
        
        # Calculate probability
        probability = round(remaining_bomb_count / len(not_nearby_tiles), 3)

        # Add probability to not-nearby tiles.
        for tile in not_nearby_tiles:
            self.change_tile_prob(tile[:2], probability)
            

    
    def make_simulation_board(self, loc):
        """
        Creates a new board to make simulations on
        """
        print("Initilizing simulation board...")
        
        # Initialize board list by iterating E's for the
        # col_count and row_count
        self.simul_board = [["E"] * (self.col_count + 2)] * (self.row_count + 2)
        
        # Check every tile on real board.
        # Replace the simulation tile with the real one.
        for i in range(1, self.row_count+1):
            for k in range(1, self.col_count+1):
                # format: [tile, num_of_probs, prob1, prob2, ... probN]
                tile = self.get_tile([i,k])
                self.simul_board[i][k] = tile
                
                
    def change_simul_F(self, loc):
        """
        Simply change the simulation tile to F (nothing else, since for
        simulation purposes only trying F is required)
        """
        self.simul_board[loc[0]][loc[1]] = "F"
        
        
    
    def simulate(self):
        """
        Simulate tile change on simulation_board(self,loc)
        
        DISCUSSION
        Make new simulation = Minesweeper(analysis=True) class?
        
        However it might be overkill if we only want to check what would
        happen next.
        
        Perhaps it would be better if we just try as "assume [loc] is a bomb
        tile. Check if remaining tiles would remain possible." (no more bombs
        left but clearly there is a bomb next to a tile which would not remain)
        
        Would it be better to write this within prob_nearby instead?
        It is, after all, specifically for whether the tiles would contradict
        if a tile were to happen to be a bomb. Proof by contradiction.
        
        Nah, let's make it a seperate function which will be used at the end
        of probability_nearby().
        
        Try making prob board of simulation, if fail, prob becomes 0 or 1.
        
        Current TODO:
            Copy current prob board and temporarily save it.
            For each unknown tile among nearby prob digits:
                Make change to prob board but do not alter real board or update from real board,
                ensure ai_next_move does not do it either.
                Iterate next moves until all nearby unknown tiles at start are filled.
                If no error is found:
                    Check a different unknown_loc to simulate flag instead.
                If an error is found:
                    Update original prob board to reflect the tiles flagged via
                    proof of contradiction. 
                    Break.
            If all moves are valid moves by the end, nothing is done.
            
        THOUGHTS
        The current problem is making the change without changing the real board
        in ai_next_move().
        Perhaps directly alter probability board? Yes, makes sense.
        Then simulated board may not be needed.
        """
        
        #self.make_simulation_board()
        #simulation = Minesweeper()
        
        # Copy current prob board and temporarily save it.
        self.original_prob_board_copy = self.prob_board.copy()
        
        # Get the digit tile with fewest unknown tiles around.
        # Minimum 2. (if 1, it would be filled anyway, not 0 because nothing left)
        for number_unknown_locs in self.digits_and_their_unknowns:
            #number = number_unknown_locs[0]
            unknown_locs = number_unknown_locs[1:]
            
            for unknown_loc in unknown_locs:
                try:
                    self.change_tile_prob(unknown_loc, 1.0)
                    # while all locs not different than unknown:
                    self.ai_next_move(simulation=True)
                except AssertionError:
                    self.prob_board = self.original_prob_board_copy
                    self.change_tile_prob(unknown_loc, 0.0)
                

        
        

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
