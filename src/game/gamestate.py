

'''
This file contains all helper functions that have to do with the tic-tac-toe game board
'''

from enum import Enum


class Tile(Enum):
    BLANK = 0
    P1 = 1
    P2 = 2


def board_contains_3_in_a_row_for_piece(board, piece):
    for row in range(3):
        if board[row][0] == board[row][1] and board[row][1] == board[row][2] and board[row][0] == piece:
            return True
    for col in range(3):
        if board[0][col] == board[1][col] and board[1][col] == board[2][col] and board[0][col] == piece:
            return True
    
    # diagonals
    if board[0][0] == board[1][1] and board [1][1] == board[2][2] and board[1][1] == piece:
        return True
    if board[2][0] == board[1][1] and board [1][1] == board[0][2] and board[1][1] == piece:
        return True
    return False



def board_contains_3_in_a_row(board):
    return board_contains_3_in_a_row_for_piece(board, Tile.P1) or board_contains_3_in_a_row_for_piece(board, Tile.P2)



def create_new_board():
    return [[Tile.BLANK for i in range(3)] for j in range(3)]