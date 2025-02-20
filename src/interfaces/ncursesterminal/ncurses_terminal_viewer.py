


import curses
from src.interfaces.ncursesterminal.ncurses_printer import *
from src.game.series_manager import InterfaceMode, SelectedTileDirections, SeriesManager

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


def direction_from_commandkey(commandkey):
    if commandkey == curses.KEY_UP:
        return SelectedTileDirections.UP
    if commandkey == curses.KEY_RIGHT:
        return SelectedTileDirections.RIGHT
    if commandkey == curses.KEY_DOWN:
        return SelectedTileDirections.DOWN
    if commandkey == curses.KEY_LEFT:
        return SelectedTileDirections.LEFT
    return SelectedTileDirections.INVALID


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

    direction = direction_from_commandkey(commandkey)
    logger.info(f"direction entered: {direction}")

    if direction != SelectedTileDirections.INVALID:
        seriesmanager.p_change_tile(direction)
    elif commandkey == 10: # 10 is used for Keyboard Enter whereas KEY_ENTER is for numpad enter
        logger.info("key is KEY_ENTER")
        seriesmanager.p_move('P')     
    # del board

def run_game_end_input(stdscr, seriesmanager):
    stdscr.clear()
    stdscr.addstr(f"{seriesmanager.most_recent_game_winner()} wins! ")
    stdscr.addstr(f"the score is now {seriesmanager.p1_score}-{seriesmanager.p2_score}")
    stdscr.addstr("   press any key to play the next round.")
    
    stdscr.getch()
    seriesmanager.next_game()


def run_match_end_input(stdscr, seriesmanager):
    stdscr.clear()
    stdscr.addstr(f"{seriesmanager.most_recent_game_winner()} wins the series! ")
    stdscr.addstr(f"the final score is: {seriesmanager.p1_score}-{seriesmanager.p2_score}")
    stdscr.addstr("press any key to return to home menu.")

    stdscr.getch()
    seriesmanager.play_another_match()
    
    

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
            case SeriesManager.game_end:
                run_game_end_input(stdscr, seriesmanager)
            case SeriesManager.match_end:
                run_match_end_input(stdscr, seriesmanager)

    # ~~~~~~~~~~~~~~~~~~~~ MAIN EXECUTION LOOP ~~~~~~~~~~~~~~~~~~

    # stdscr.addstr("curses mode activated")
    # stdscr.refresh()

    # ~~~~~~~~~~~~~~~~~~~~ EXIT NCURSES MODE ~~~~~~~~~~~~~~~~~~~
    # curses.nocbreak()
    # stdscr.keypad(False)
    # curses.echo()



def enter_ncurses_mode_wrapper(seriesmanager):
    curses.wrapper(enter_ncurses_mode, seriesmanager)
    