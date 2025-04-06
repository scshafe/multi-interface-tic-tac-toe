
import curses

from src.game.gamestate import Tile

SQUARE_WIDTH_ROOT = 6
SQUARE_HEIGHT_ROOT = 7

# mulitplier will eventually be dynamic for adjusting size of screen to make board bigger
MULTIPLIER = 1

SQUARE_WIDTH = SQUARE_WIDTH_ROOT * MULTIPLIER
SQUARE_HEIGHT = SQUARE_HEIGHT_ROOT * MULTIPLIER





def print_menu_screen(seriesmanager):
    
    return f"Welcome to Tic-Tac-Toe!\n\nPlayer 1: {seriesmanager.p1_name}\nPlayer 2: {seriesmanager.p2_name}\n\n[P] to play\n[C] to change names\n[I] change interfaces"


blank = ["      ",
         "      ",
         "      ",
         "      ",
         "      ",
         "      "]

circle = ["  __  ",
          ' /  \\ ',
          '/    \\',
          '\\    /',
          ' \\__/ ',
          "      "]

cross = ["      ",
         ' \\  / ',
         '  \\/  ',
         '  /\\  ',
         ' /  \\ ',
         "      "]


# ------------ EVENTUALLY WILL SWITCH TO THIS STYLE -------------

# SIZING RULES: each size up (controlled by hitting '+') will result in a change in n
# n is the underlying size from which characters and spaces are calculated

# O will be given by:



# X will be given by:


# 3x3    2x2
#  _
# / \    \/
# \_/    /\

# 1 taller results in +2 to both dimensions
#  5x5      4x4
#   _
#  / \    \  /
# /   \    \/
# \   /    /\
#  \_/    /  \

# 1 wider results in +1 just to width
#   5x6        4x5
#    __
#   /  \    \   /
#  /    \    \_/
#  \    /    / \
#   \__/    /   \

# 1 taller results in +2 to both dimensions
#   7x8        6x6
#    __
#   /  \    \     /
#  /    \    \   /
# /      \    \_/
# \      /    / \
#  \    /    /   \
#   \__/    /     \


def build_board_string(seriesmanager, game_won=False, flashing=False):

    output = ""

    for row in range(3):
        for square_height_mod in range(len(circle)+2):
            for col in range(3):
    
                if square_height_mod == 0 or square_height_mod == (len(circle) + 1):
                    if not game_won and seriesmanager.selected_tile_map[row][col] == True:
                        output = output + "--------"
                    else:
                        output = output + "        "
                
                
                else:
                    square_height = square_height_mod - 1
                    tmp_border = '|' if seriesmanager.selected_tile_map[row][col] and not game_won else ' '
                    output = output + tmp_border

                    if seriesmanager.board[row][col] == Tile.BLANK or (flashing == True and seriesmanager.win[row][col] == True):
                        output = output + blank[square_height]
                    elif seriesmanager.board[row][col] == Tile.P1:
                        output = output + cross[square_height]
                    elif seriesmanager.board[row][col] == Tile.P2:
                        output = output + circle[square_height]
                    else:
                        print("ERROR!!!")
                        # quit()
                
                    output = output + tmp_border

                
                if col < 2:
                    output = output + '|'     
        if row < 2:
            output = output + '--------------------------'
    return output

# 1
#----
#|/\|
#|\/|
#----

# 2
#------
#| /\ |
#|/  \|
#|\  /|
#| \/ |
#------


def create_circle_piece(size):
    circle = [[" " for i in range(size*2)] for j in range(size*2)]
    for i in range(size):
        # top left
        it_left = size-1-i
        it_right = size + i
        circle[i][it_left] = '/'
        #top right
        circle[i][it_right] = '\\'
        # bottom left
        circle[size-1-i][it_left] = '\\'
        # bottom right
        circle[size-1-i][it_right] = '/'
    return circle      



def build_sized_board_string(seriesmanager, game_won=False, flashing=False, size=3):
    
    output = ""
    
    tile_height = (size*2) + 2 # +2 is for the border for spaces or outline of selected tile
    select_border = "-"*tile_height
    space_border = " "*tile_height
    row_divider = "-"*((tile_height*3) + 2)


    for row in range(3):
        for square_height_mod in range(tile_height):
            for col in range(3):
    
                if square_height_mod == 0 or square_height_mod == tile_height:
                    if not game_won and seriesmanager.selected_tile_map[row][col] == True:
                        output = output + select_border
                    else:
                        output = output + space_border
                
                
                else:
                    square_height = square_height_mod - 1  # square height is for the character itself (ignoring the space/selected boundary)
                    tmp_border = '|' if seriesmanager.selected_tile_map[row][col] and not game_won else ' '
                    output = output + tmp_border

                    if seriesmanager.board[row][col] == Tile.BLANK or (flashing == True and seriesmanager.win[row][col] == True):
                        output = output + blank[square_height]
                    elif seriesmanager.board[row][col] == Tile.P1:
                        output = output + cross[square_height]
                    elif seriesmanager.board[row][col] == Tile.P2:
                        output = output + circle[square_height]
                    else:
                        print("ERROR!!!")
                        # quit()
                
                    output = output + tmp_border

                
                if col < 2:
                    output = output + '|'     
        if row < 2:
            output = output + row_divider
    return output

