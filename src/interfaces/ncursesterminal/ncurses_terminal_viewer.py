


import curses
from src.interfaces.ncursesterminal.ncurses_printer import *
from src.game.series_manager import InterfaceMode, SeriesManager

from src.logging.my_logging import logger




def run_menu_screen_input(stdscr, seriesmanager):

    logger.info("entering run_menu_screen_input")
    
    stdscr.clear()
    stdscr.addstr(print_menu_screen(seriesmanager))
    stdscr.refresh()
    commandkey = stdscr.getkey()
    if commandkey == "p":
    # if commandkey == ord("p"):
        seriesmanager.play_game()
        
    # match commandkey:
    #     case ord("p"):
    #         seriesmanager.play_game()
    #     case "C":
    #         seriesmanager.play_game()
    #     case "I":
    #         seriesmanager.play_game()
    #     case _:
    #         # error_input_message()
    #         return


def run_player_turn(stdscr, seriesmanager, player_turn):
    logger.info(f"entering run_player_turn [{player_turn}]")
    stdscr.clear()

    board = curses.newwin(34, 26, 0,0)
    board.keypad(True)

    board_string = build_board_string(seriesmanager)
    board.addstr(board_string)
    board.refresh()
    
    commandkey = board.getch()

    logger.info(f"{player_turn} entered input: {commandkey}")

    if commandkey == curses.KEY_RIGHT:
        board.addstr("test")
        board.refresh()
        

        seriesmanager.p_change_tile(commandkey, board)
    
    del board

    
    

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
    stdscr.keypad(True)

    stdscr.clear()

    # stdscr.addstr("Pretty text")
    # stdscr.refresh()

    # board = curses.newwin((3 * SQUARE_HEIGHT) + 2, (3 * SQUARE_WIDTH + 2), 0,0)

    # commandbar = curses.newwin(3, curses.COLS, 3 * SQUARE_HEIGHT + 2, 0)
    
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

    # board = build_board_string(seriesmanager)
    # print(board)
        
    while (seriesmanager.interface_mode == InterfaceMode.NCURSES):
        
        current_state = seriesmanager.current_state

        match current_state:
            case SeriesManager.menu_screen:
                run_menu_screen_input(stdscr, seriesmanager)
            # case SeriesManager.interface_screen:
            #     run_interface_screen(seriesmanager)
            # case SeriesManager.change_name:
            #     change_name_screen(seriesmanager)
            case SeriesManager.p1_turn:
                run_player_turn(stdscr, seriesmanager, 1)
            case SeriesManager.p2_turn:
                run_player_turn(stdscr, seriesmanager, 2)
            # case SeriesManager.game_end:
            #     run_game_end_input(seriesmanager)
            # case SeriesManager.match_end:
            #     run_match_end_input(seriesmanager)

    # ~~~~~~~~~~~~~~~~~~~~ MAIN EXECUTION LOOP ~~~~~~~~~~~~~~~~~~

    # stdscr.addstr("curses mode activated")
    # stdscr.refresh()

    # ~~~~~~~~~~~~~~~~~~~~ EXIT NCURSES MODE ~~~~~~~~~~~~~~~~~~~
    # curses.nocbreak()
    # stdscr.keypad(False)
    # curses.echo()



def enter_ncurses_mode_wrapper(seriesmanager):
    curses.wrapper(enter_ncurses_mode, seriesmanager)
    