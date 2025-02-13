
import curses

SQUARE_WIDTH_ROOT = 8
SQUARE_HEIGHT_ROOT = 6

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

circle = ["        ",
          "  __  ",
          " /  \ ",
          "/    \\",
          "\\    /",
          " \\__/ ",
          "      "]

cross = ["      ",
         " \\  / ",
         "  \\/  ",
         "  /\\  ",
         " /  \\ ",
         "      ",
         "      "]





def build_board_string(seriesmanager):

    output = ""

    for row in range(2):
        for square_height in range(len(circle)):
            for col in range(2):
                square = col + (row * 3)

                if seriesmanager.board[square] == ' ':
                    output = output + blank[square_height]
                elif seriesmanager.board[square] == 'X':
                    output = output + cross[square_height]
                elif seriesmanager.board[square] == 'O':
                    output = output + circle[square_height]
                else:
                    print("ERROR!!!")
                    quit()
                
                if col != 2:
                    output = output + '|'     
        if row != 2:
            output = output + '--------------------'
    return output




