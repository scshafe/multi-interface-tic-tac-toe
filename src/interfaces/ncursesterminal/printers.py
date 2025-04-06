
import curses

from src.game.gamestate import Tile
from src.logging.my_logging import logger


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

def create_blank_piece(size):
    blank = [[" " for i in range(size*2)] for j in range(size*2)]
    return blank


def create_circle_piece(size):
    circle = [[" " for i in range(size*2)] for j in range(size*2)]
    for i in range(size):
        it_left = size-1-i
        it_right = size + i
        # top left
        circle[i][it_left] = '/'
        #top right
        circle[i][it_right] = '\\'
        # bottom left
        circle[len(circle)-1-i][it_left] = '\\'
        # bottom right
        circle[len(circle)-1-i][it_right] = '/'
    return circle      


def create_cross_piece(size):
    cross = [[" " for i in range(size*2)] for j in range(size*2)]
    for i in range(size):
        it_left = i
        it_right = len(cross)-1-i
        #top left
        cross[i][it_left] = '\\'
        #top right
        cross[i][it_right] = '/'
        #bottom left
        cross[len(cross)-1-i][it_left] = '/'
        #bottom right
        cross[len(cross)-1-i][it_right] = '\\'
    return cross



def build_size_row(seriesmanager, row, game_won=False, flashing=False, size=2):
    output = ""
    tile_height = (size*2) + 2 # +2 is for the border for spaces or outline of selected tile
    select_border = "-"*tile_height
    space_border = " "*tile_height
    row_divider = "-"*((tile_height*3) + 2)


    logger.info(size)
    circle = create_circle_piece(size)
    cross = create_cross_piece(size)
    blank = create_blank_piece(size)


    logger.info(f"circle: {circle}")
    logger.info(f"cross: {cross}")
    logger.info(f"blank: {blank}")

    for square_height_mod in range(tile_height):
        logger.info(f"square_height_mod: {square_height_mod}")
        for col in range(3):

            if square_height_mod == 0 or square_height_mod == tile_height-1:
                if not game_won and seriesmanager.selected_tile_map[row][col] == True:
                    output = output + select_border
                else:
                    output = output + space_border
            
            
            else:
                
                square_height = square_height_mod - 1  # square height is for the character itself (ignoring the space/selected boundary)
                logger.info(f"square height: {square_height}")
                tmp_border = '|' if seriesmanager.selected_tile_map[row][col] and not game_won else ' '
                output = output + tmp_border
                if seriesmanager.board[row][col] == Tile.BLANK or (flashing == True and seriesmanager.win[row][col] == True):
                    output = output + ''.join(blank[square_height])
                elif seriesmanager.board[row][col] == Tile.P1:
                    output = output + ''.join(cross[square_height])
                elif seriesmanager.board[row][col] == Tile.P2:
                    output = output + ''.join(circle[square_height])
                else:
                    print("ERROR!!!")
                    # quit()
            
                output = output + tmp_border
            
            if col < 2:
                output = output + '|'     
    return output


def log_board(board, size):
    tile_width = (size*2)+2
    board_width = (tile_width*3)+2

    logger.info("Printing Board")   
    for i in range(0, len(board), board_width):
        logger.info(''.join(board[i:i+board_width]))

    

def build_sized_board_string(seriesmanager, game_won=False, flashing=False, size=2):
    output = ""
    tile_height = (size*2) + 2 # +2 is for the border for spaces or outline of selected tile
    logger.info(f"tile_height: {tile_height}")
    row_divider = "-"*((tile_height*3) + 2)
    logger.info(f"size: {size}")

    for row in range(3):
        output = output + build_size_row(seriesmanager, row, game_won, flashing, size)
        if row < 2:
            output = output + row_divider
    log_board(output, size)
    return output



