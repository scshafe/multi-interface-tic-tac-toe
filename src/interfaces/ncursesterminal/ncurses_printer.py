
import curses

SQUARE_WIDTH_ROOT = 6
SQUARE_HEIGHT_ROOT = 7

# mulitplier will eventually be dynamic for adjusting size of screen to make board bigger
MULTIPLIER = 1

SQUARE_WIDTH = SQUARE_WIDTH_ROOT * MULTIPLIER
SQUARE_HEIGHT = SQUARE_HEIGHT_ROOT * MULTIPLIER





def print_menu_screen(seriesmanager):
    
    return "[P] to play"


blank = ["      ",
         "      ",
         "      ",
         "      ",
         "      ",
         "      ",
         "      "]

circle = ["      ",
          "  __  ",
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
         "      ",
         "      "]





def build_board_string(seriesmanager):

    output = ""

    for row in range(3):
        for square_height_mod in range(len(circle)+2):
            for col in range(3):

                if square_height_mod == 0 or square_height_mod == (len(circle) + 1):
                    if seriesmanager.selected_tile_map[row][col]:
                        output = output + "--------"
                    else:
                        output = output + "        "
                
                
                else:
                    square_height = square_height_mod - 1
                    output = output + '|' if seriesmanager.selected_tile_map[row][col] else output + ' '

                    if seriesmanager.board[row][col] == ' ':
                        output = output + blank[square_height]
                    elif seriesmanager.board[row][col] == 'X':
                        output = output + cross[square_height]
                    elif seriesmanager.board[row][col] == 'O':
                        output = output + circle[square_height]
                    else:
                        print("ERROR!!!")
                        # quit()
                
                    output = output + '|' if seriesmanager.selected_tile_map[row][col] else output + ' '
                
                if col < 2:
                    output = output + '|'     
        if row < 2:
            output = output + '--------------------------'
    return output




