


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
    commandkey = commandkey.lower()
    match commandkey:
        case "p":
            seriesmanager.play_game()
        case "c":
            seriesmanager.change_names()
        case "i":
            seriesmanager.change_interface()

        case _:
            return


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

def run_game_end_input(stdscr, seriesmanager):
    stdscr.clear()
    stdscr.addstr(f"{seriesmanager.most_recent_game_winner()} wins! ")
    stdscr.addstr(f"the score is now {seriesmanager.p1_score}-{seriesmanager.p2_score}\n")
    stdscr.addstr("   press any key to play the next round.")
    
    stdscr.getch()
    seriesmanager.next_game()


def run_match_end_input(stdscr, seriesmanager):
    stdscr.clear()
    stdscr.addstr(f"{seriesmanager.most_recent_game_winner()} wins the series! ")
    stdscr.addstr(f"the final score is: {seriesmanager.p1_score}-{seriesmanager.p2_score}\n")
    stdscr.addstr("press any key to return to home menu.")

    stdscr.getch()
    seriesmanager.play_another_match()
    
    
def run_interface_screen(stdscr, seriesmanager):
    stdscr.clear()
    stdscr.addstr(f"which interface would you like to use?\n[1] Simple\n[2] NCurses\n[3] GTK Gui\n[4] Quit")

    commandkey = stdscr.getkey()
    seriesmanager.interface_selected(commandkey)

def change_name_screen(stdscr, seriesmanager):
    stdscr.clear()
    stdscr.addstr(f"which player would you like to change the name for? [1/2]")
    player_num = stdscr.getkey()
    stdscr.addstr(f"\nchanging name for {seriesmanager.p1_name if player_num == "1" else seriesmanager.p2_name}: ")
    curses.echo()
    new_name = stdscr.getstr()
    curses.noecho()

    seriesmanager.change_new_name(player_num, new_name)



def enter_ncurses_mode(stdscr, seriesmanager):
    stdscr.keypad(True)
        
    while (seriesmanager.interface_mode == InterfaceMode.NCURSES):
        
        current_state = seriesmanager.current_state

        match current_state:
            case SeriesManager.menu_screen:
                run_menu_screen_input(stdscr, seriesmanager)
            case SeriesManager.interface_screen:
                run_interface_screen(stdscr, seriesmanager)
            case SeriesManager.change_name:
                change_name_screen(stdscr, seriesmanager)
            case SeriesManager.p1_turn:
                run_player_turn(stdscr, seriesmanager, 1)
            case SeriesManager.p2_turn:
                run_player_turn(stdscr, seriesmanager, 2)
            case SeriesManager.game_end:
                run_game_end_input(stdscr, seriesmanager)
            case SeriesManager.match_end:
                run_match_end_input(stdscr, seriesmanager)



def enter_ncurses_mode_wrapper(seriesmanager):
    curses.wrapper(enter_ncurses_mode, seriesmanager)
    