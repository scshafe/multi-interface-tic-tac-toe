
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




