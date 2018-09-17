#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 12:29:53 2018

@author: Denizhan Akar

DESCRIPTION
An AI made from the principles which guarantee as much success as possible.

GAME: Minesweeper
INFORMATION TYPE: Perfect Information

TODO
Formalize rules of game:
    Make 2 modes:
        (DONE) Play minesweeper on python
        Parse screen data and play
Use OpenCV to get Minesweeper game data from screen.
Process data into internal data representation

Use Probability Theory to make wise choice
"""
# Import modules.
from Minesweeper import Minesweeper
from Minesweeper_with_AI import Minesweeper_with_AI

# Game constants
row_count = 8
col_count = 8
activity_mode = "game"  # game/analysis/parse_board/parse_window
seed = 1
bomb_locations = [
    [1, 1],
    [2, 3],
]  # [4,1], [2,3], [2,5], [3,6], [3,5]] # If specific loc bombs, change activity to "anaylsis"
total_bomb_count = 10  # If random bombs, change total_bomb_count and activity to "game"

test_board_for_not_prob = [
    ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E"],
    ["E", "E", "E", "E", "E", "2", ["F", "B"], "?", "?", "E"],
    ["E", "E", "E", "1", "1", "3", ["F", "B"], "2", "?", "E"],
    ["E", "E", "E", "1", ["F", "B"], "2", "1", "1", "?", "E"],
    ["E", "1", "2", "3", "3", "2", "2", "1", "?", "E"],
    ["E", "?", ["?", "B"], ["?", "B"], "?", ["?", "B"], "?", ["?", "B"], "?", "E"],
    ["E", "?", "2", "?", ["?", "B"], "?", "?", "?", ["?", "B"], "E"],
    ["E", "?", "?", "?", "?", "?", "?", "?", "?", "E"],
    ["E", "?", ["?", "B"], "?", "?", "?", "?", "?", "?", "E"],
    ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E"],
]

game = Minesweeper_with_AI(
    row_count,
    col_count,
    activity_mode,
    total_bomb_count = total_bomb_count,
    seed = seed,
    bomb_locations=bomb_locations,
    board=test_board_for_not_prob,
)
