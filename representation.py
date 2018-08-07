#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 00:08:29 2018

@author: denizhan
"""

# Internal Representation of Game

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

def print_board(board):
    """
    Function to print board
    """
    for row in board:
        print((" ".join(row)))
    print()

def get_tile(tile_loc, board):
    return board[tile_loc[0]][tile_loc[1]]

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
    
if __name__ == "__main__":
    board = make_board()
    print_board(board)
    board = change_tile([1,3], "F", board)
    print_board(board)