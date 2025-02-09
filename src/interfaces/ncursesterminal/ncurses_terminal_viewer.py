
import curses
from src.game.series_manager import InterfaceMode, SeriesManager

SQUARE_WIDTH_ROOT = 8
SQUARE_HEIGHT_ROOT = 6

# mulitplier will eventually be dynamic for adjusting size of screen to make board bigger
MULTIPLIER = 3

SQUARE_WIDTH = SQUARE_WIDTH_ROOT * MULTIPLIER
SQUARE_HEIGHT = SQUARE_HEIGHT_ROOT * MULTIPLIER


def run_menu_screen_input(seriesmanager, commandkey):
    match commandkey:
        case "P":
            seriesmanager.play_game()
        case _:
            return



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

    board = curses.newwin((3 * SQUARE_HEIGHT) + 2, (3 * SQUARE_WIDTH + 2), 0,0)

    commandbar = curses.newwin(3, curses.COLS, 3 * SQUARE_HEIGHT + 2, 0)
    
    stdscr.refresh()
    
    # while True:
    #     # Menu keys
    #     c = stdscr.getch()
    #     if c == ord('m'):
    #         board.addstr("m detected")
    #         board.refresh()
    #     if c == ord('')


    #     if c == curses.KEY_LEFT:
    #         commandbar.addstr("left")
    #         commandbar.refresh()

        
    while (seriesmanager.interface_mode == InterfaceMode.NCURSES):
        input(run_match_end_input_string(seriesmanager))
        
        current_state = seriesmanager.current_state
        commandkey = stdscr.getch()
        match current_state:
            case SeriesManager.menu_screen:
                run_menu_screen_input(seriesmanager, commandkey)
            case SeriesManager.interface_screen:
                run_interface_screen(seriesmanager)
            case SeriesManager.change_name:
                change_name_screen(seriesmanager)
            case SeriesManager.p1_turn:
                run_player_turn(seriesmanager, 1)
            case SeriesManager.p2_turn:
                run_player_turn(seriesmanager, 2)
            case SeriesManager.game_end:
                run_game_end_input(seriesmanager)
            case SeriesManager.match_end:
                run_match_end_input(seriesmanager)

    # ~~~~~~~~~~~~~~~~~~~~ MAIN EXECUTION LOOP ~~~~~~~~~~~~~~~~~~

    # stdscr.addstr("curses mode activated")
    # stdscr.refresh()

    # ~~~~~~~~~~~~~~~~~~~~ EXIT NCURSES MODE ~~~~~~~~~~~~~~~~~~~
    # curses.nocbreak()
    # stdscr.keypad(False)
    # curses.echo()



def enter_ncurses_mode_wrapper(seriesmanager):
    curses.wrapper(enter_ncurses_mode, seriesmanager)