#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 12:29:53 2018

@author: Denizhan Akar

Description
An AI made from the principles which guarantee as much success as possible.

@TODO, by priority

Construct internal data representation of game
Formalize rules of game
Formalize strategy to win game
    Choose starting locations anywhere other than middle
    For now choose just 4. If blank space is not found, continue pressing.
    
    Only consider empty tiles 
    
    If the number of empty tiles around warning number is equal to the 
    warning number minus bomb tiles flagged around it, they are bombs.
    
    If the 

Use OpenCV to take minesweeper game data
Process data into internal data representation

Use Probability Theory to make wise choice

"""
# %% Internal Representation of Game

# Board constants
board = []
row_count = 8
col_count = 8

# Construct base board
for i in range(row_count):
    board.append("?" * col_count)

# Function to print board
def print_board(board):
    for row in board:
        print((" ".join(row)))
        
print_board(board)


def make_move

# Formalized Rules of Game


# Formalized Strategy












