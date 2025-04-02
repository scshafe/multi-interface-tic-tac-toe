


import curses
from src.interfaces.ncursesterminal.printers import *
from src.interfaces.ncursesterminal.input_validators import *
from src.game.series_manager import InterfaceMode, SelectedTileDirections, SeriesManager

from src.logging.my_logging import logger


def get_valid_input(stdscr, validator):
    inputkey = stdscr.getch()
    
    if inputkey == curses.KEY_RESIZE:
        logger.info("Resizing")
        return False, inputkey
    elif inputkey < 256:
        logger.info(f"Char entered: {chr(inputkey)} from input: {inputkey}")
        inputkey = chr(inputkey)
        return validator(inputkey), inputkey
    else:
        logger.info(f"Special key: {inputkey}")
        return validator(inputkey), inputkey



def run_menu_screen_input(stdscr, seriesmanager):

    logger.info("entering run_menu_screen_input")
    
    stdscr.clear()
    stdscr.addstr(print_menu_screen(seriesmanager))
    
    is_valid, commandkey = get_valid_input(stdscr, menu_screen_validator)
    if not is_valid:
        return
    commandkey = commandkey.lower()
    match commandkey:
        case "p":
            seriesmanager.play_game()
        case "c":
            seriesmanager.change_player_name()
        case "i":
            seriesmanager.change_interface()
        case "q":
            seriesmanager.quit_game()
        case _:
            logger.error("run_menu_screen_input case _ reached")


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
    stdscr.refresh()

    height, width = stdscr.getmaxyx()
    logger.info(f"height: {height}\nwidth: {width}")
    
    height_border = int((height - 34) / 2)
    width_border = int((width - 26) / 2)


    board = curses.newwin(34, 26, height_border, width_border)
    board.keypad(True)

    board_string = build_board_string(seriesmanager)
    board.addstr(board_string)
    board.refresh()
    
    is_valid, commandkey = get_valid_input(board, run_player_turn_validator)
#    commandkey = board.getch()
    logger.info(f"{player_turn} entered input: {commandkey}")

    direction = direction_from_commandkey(commandkey)
    logger.info(f"direction entered: {direction}")

    if direction != SelectedTileDirections.INVALID:
        logger.info(f"changed selected tile: {direction}")
        seriesmanager.p_change_tile(direction)
    elif commandkey == chr(10): # 10 is used for Keyboard Enter whereas KEY_ENTER is for numpad enter
        logger.info("key is KEY_ENTER")
        seriesmanager.p_move('P')
    else:
        logger.info(f"invalid player_turn input: {commandkey}")

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

def select_change_name_screen(stdscr, seriesmanager):
    stdscr.clear()
    stdscr.addstr(f"which player would you like to change the name for? [1/2]")
    player_num = stdscr.getkey()
    stdscr.addstr(f"\nchanging name for {seriesmanager.p1_name if player_num == "1" else seriesmanager.p2_name}: ")
    player_num = True if player_num == "1" else False
    seriesmanager.select_player_name_change(player_num)


def enter_change_name_screen(stdscr, seriesmanager):
    stdscr.clear()
    stdscr.addstr(f"Changing name to: ")
    curses.echo()
    new_name = stdscr.getstr().decode('utf-8')
    curses.noecho()

    seriesmanager.enter_player_name_change(new_name)


def paint_ncurses_screen(stdscr, seriesmanager):
   current_state = seriesmanager.current_state
   match current_state:
        case SeriesManager.menu_screen:
            run_menu_screen_input(stdscr, seriesmanager)
        case SeriesManager.interface_screen:
            run_interface_screen(stdscr, seriesmanager)
        case SeriesManager.select_change_name:
            select_change_name_screen(stdscr, seriesmanager)
        case SeriesManager.enter_change_name:
            enter_change_name_screen(stdscr, seriesmanager)
        case SeriesManager.p1_turn:
            run_player_turn(stdscr, seriesmanager, 1)
        case SeriesManager.p2_turn:
            run_player_turn(stdscr, seriesmanager, 2)
        case SeriesManager.game_end:
            run_game_end_input(stdscr, seriesmanager)
        case SeriesManager.match_end:
            run_match_end_input(stdscr, seriesmanager)



def enter_ncurses_mode(stdscr, seriesmanager):
    stdscr.keypad(True)
        
    while (seriesmanager.interface_mode == InterfaceMode.NCURSES):
        paint_ncurses_screen(stdscr, seriesmanager)        



def enter_ncurses_mode_wrapper(seriesmanager):
    curses.wrapper(enter_ncurses_mode, seriesmanager)
    
