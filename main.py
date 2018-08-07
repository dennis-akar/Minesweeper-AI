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
# Main Executor

# Import own modules
import representation as rep
import rules as rul
import strategy as strat

# Game constants
row_count = 8
col_count = 8

board = rep.make_board(row_count, col_count)

board = strat.change_random_tiles(row_count, col_count, board)

#board = strat.unknowns_around_equal_to_number_tile(board)

board = strat.probability_nearby(board)

rep.print_board(board)


