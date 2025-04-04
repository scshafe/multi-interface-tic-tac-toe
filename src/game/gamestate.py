

'''
This file contains all helper functions that have to do with the tic-tac-toe game board
'''

from enum import Enum


class Tile(Enum):
    BLANK = 0
    P1 = 1
    P2 = 2


def board_contains_3_in_a_row_for_piece(board, piece):
    win = [[False for i in range(3)] for j in range(3)]
    for row in range(3):
        if board[row][0] == board[row][1] and board[row][1] == board[row][2] and board[row][0] == piece:
            win[row][0] = win[row][1] = win[row][2] = True
            return win
    for col in range(3):
        if board[0][col] == board[1][col] and board[1][col] == board[2][col] and board[0][col] == piece:
            win[0][col] = win[1][col] = win[2][col] = True
            return win
    
    # diagonals
    if board[0][0] == board[1][1] and board [1][1] == board[2][2] and board[1][1] == piece:
        win[0][0] = win[1][1] = win[2][2] = True
        return win
    if board[2][0] == board[1][1] and board [1][1] == board[0][2] and board[1][1] == piece:
        win[2][0] = win[1][1] = win[0][2] = True
        return win
    return []



def board_contains_3_in_a_row(board):
    return board_contains_3_in_a_row_for_piece(board, Tile.P1) + board_contains_3_in_a_row_for_piece(board, Tile.P2)



def create_new_board():
    return [[Tile.BLANK for i in range(3)] for j in range(3)]
