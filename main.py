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

Total conversion to class based system?
- No need to constantly insert board parameter.
- Methods work more intricately.

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
"""
This is to serve as the main decision flow of the program.
"""

# If random bombs, change total_bomb_count and activity to game
# If specific loc bombs, change bomb_loc and activity to anaylsis

# Import own modules
from Minesweeper import Minesweeper
from Minesweeper_with_AI import Minesweeper_with_AI

# Game constants
row_count = 8
col_count = 8
activity_mode = "parse_board"  # game/analysis/parse_board/parse_window
bomb_locations = [[1,1], [2,3]] #[4,1], [2,3], [2,5], [3,6], [3,5]]
total_bomb_count = 10

test_board_for_not_prob = [['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
 ['E', 'E', 'E', 'E', 'E', '2', ['F', 'B'], '?', '?', 'E'],
 ['E', 'E', 'E', '1', '1', '3', ['F', 'B'], '2', '?', 'E'],
 ['E', 'E', 'E', '1', ['F', 'B'], '2', '1', '1', '?', 'E'],
 ['E', '1', '2', '3', '3', '2', '2', '1', '?', 'E'],
 ['E',
  '?',
  ['?', 'B'],
  ['?', 'B'],
  '?',
  ['?', 'B'],
  '?',
  ['?', 'B'],
  '?',
  'E'],
 ['E', '?', '2', '?', ['?', 'B'], '?', '?', '?', ['?', 'B'], 'E'],
 ['E', '?', '?', '?', '?', '?', '?', '?', '?', 'E'],
 ['E', '?', ['?', 'B'], '?', '?', '?', '?', '?', '?', 'E'],
 ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E']]

game = Minesweeper_with_AI(row_count, col_count, activity_mode, 
                           total_bomb_count=total_bomb_count,
                           bomb_locations=bomb_locations,
                           board=test_board_for_not_prob)
