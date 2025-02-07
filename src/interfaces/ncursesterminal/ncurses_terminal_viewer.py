
import curses

SQUARE_WIDTH_ROOT = 8
SQUARE_HEIGHT_ROOT = 6

# mulitplier will eventually be dynamic for adjusting size of screen to make board bigger
MULTIPLIER = 3

SQUARE_WIDTH = SQUARE_WIDTH_ROOT * MULTIPLIER
SQUARE_HEIGHT = SQUARE_HEIGHT_ROOT * MULTIPLIER






def enter_ncurses_mode(stdscr, seriesmanager):

    # ~~~~~~~~~~~~~~~~~~~~ SETUP NCURSES MODE ~~~~~~~~~~~~~~~~~~~

    # stdscr = curses.initscr()

    # turns off automatic ehcoing of keys to the screen
    # curses.noecho()

    # react to keys instantly, without require the [Enter] key to be pressed
    # curses.cbreak()

    # return special value such as `curses.KEY_LEFT` intead of multibyte escape sequence
    # curses.keypad(True)
    # curses.echo()

    stdscr.clear()

    stdscr.addstr("Pretty text")
    stdscr.refresh()

    # print("Entered ncurses mode: ", seriesmanager.interface_mode)
    # print(f"curses size: {curses.LINES} rows, {curses.COLS} cols")

    board = curses.newwin((3 * SQUARE_HEIGHT) + 2, (3 * SQUARE_WIDTH + 2), 0,0)

    commandbar = curses.newwin(3, curses.COLS, 3 * SQUARE_HEIGHT + 2, 0)
    
    stdscr.refresh()
    
    while True:
        c = stdscr.getch()
        if c == ord('m'):
            board.addstr("m detected")
            board.refresh()
        
        if c == curses.KEY_LEFT:
            commandbar.addstr("left")
            commandbar.refresh()

        

    # ~~~~~~~~~~~~~~~~~~~~ MAIN EXECUTION LOOP ~~~~~~~~~~~~~~~~~~

    # stdscr.addstr("curses mode activated")
    # stdscr.refresh()

    # ~~~~~~~~~~~~~~~~~~~~ EXIT NCURSES MODE ~~~~~~~~~~~~~~~~~~~
    # curses.nocbreak()
    # stdscr.keypad(False)
    # curses.echo()



def enter_ncurses_mode_wrapper(seriesmanager):
    curses.wrapper(enter_ncurses_mode, seriesmanager)