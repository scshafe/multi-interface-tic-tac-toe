

import time
import curses
from src.interfaces.ncursesterminal.printers import *
from src.interfaces.ncursesterminal.input_validators import *
from src.game.series_manager import InterfaceMode, SelectedTileDirections, SeriesManager

from src.logging.my_logging import logger


class CursesGUI:
    def __init__(self, seriesmanager, size=2):
        self.seriesmanager = seriesmanager
        self.size = size
        self.tile_height = (size*2)+2
        #self.height is height of screen
        #self.width is width of screen

    # center many lines of text from a list each on their own line (with a 2 space y-pad in the beginning)
    def center_lines_of_text(self, window, text):
        height, width = window.getmaxyx()
        
        y = 2
        for line in text:
            x = width // 2 - len(line) // 2
            window.addstr(y, x, line)
            y+=1
        window.refresh()

    def get_valid_input(self, stdscr, screen_options):
        inputkey = stdscr.getch()
        
        if inputkey == curses.KEY_RESIZE:
            logger.info("Resizing")
        elif validator(inputkey, screen_options):
            logger.info(f"Special key: {inputkey}")
            return True, inputkey
        elif validator(chr(inputkey).lower(), screen_options):
            logger.info(f"Chr key: {chr(inputkey)}")
            return True, chr(inputkey).lower()
        else:
            logger.error(f"Invalid input. Raw: {inputkey}, chr form: {chr(inputkey)}")
        return False, inputkey

    def run_menu_screen_input(self, stdscr):

        logger.info("entering self.run_menu_screen_input")
        
        stdscr.clear()
        stdscr.addstr(print_menu_screen(self.seriesmanager))
        
        is_valid, commandkey = self.get_valid_input(stdscr, menu_screen_options)
        if not is_valid:
            return
        match commandkey:
            case "p":
                self.seriesmanager.play_game()
            case "c":
                self.seriesmanager.change_player_name()
            case "i":
                self.seriesmanager.change_interface()
            case "q":
                self.seriesmanager.quit_game()
            case _:
                logger.error("self.run_menu_screen_input case _ reached")


    def direction_from_commandkey(self, commandkey):
        if commandkey == curses.KEY_UP:
            return SelectedTileDirections.UP
        if commandkey == curses.KEY_RIGHT:
            return SelectedTileDirections.RIGHT
        if commandkey == curses.KEY_DOWN:
            return SelectedTileDirections.DOWN
        if commandkey == curses.KEY_LEFT:
            return SelectedTileDirections.LEFT
        return SelectedTileDirections.INVALID


    def get_board(self, stdscr):
        height, width = stdscr.getmaxyx()
        logger.info(f"height: {height}\nwidth: {width}")
        
        height_border = int((height - 34) / 2)
        width_border = int((width - 26) / 2)
        

        #board = curses.newwin(34, 26, height_border, width_border)
        board = curses.newwin(21, 20, height_border, width_border)
        board.keypad(True)

        message_box = curses.newwin(10, width, 21 + height_border + 1, 0)
        return board, message_box

    def run_player_turn(self, stdscr, player_turn):
        logger.info(f"entering self.run_player_turn [{player_turn}]")
        stdscr.clear()
        stdscr.refresh()
        board, message_box = self.get_board(stdscr)
        board_string = build_sized_board_string(self.seriesmanager)
        board.addstr(board_string)
        board.refresh()

        text = ["use [arrows] to move selected tile", "press [enter] to place piece", "press [m] to return to the menu screen"]
        self.center_lines_of_text(message_box, text)
        is_valid, commandkey = self.get_valid_input(board, run_player_turn_options)
        if not is_valid:
            return
                
    #    commandkey = board.getch()
        logger.info(f"{player_turn} entered input: {commandkey}")

        direction = self.direction_from_commandkey(commandkey)
        logger.info(f"direction entered: {direction}")

        if direction != SelectedTileDirections.INVALID:
            logger.info(f"changed selected tile: {direction}")
            self.seriesmanager.p_change_tile(direction)
        elif commandkey == 10: # 10 is used for Keyboard Enter whereas KEY_ENTER is for numpad enter
            logger.info("key is KEY_ENTER")
            self.seriesmanager.p_move('P')
        elif commandkey == "m":
            self.seriesmanager.open_menu()
        else:
            logger.info(f"invalid player_turn input: {commandkey}")


    def display_flashing_board(self, stdscr, message_list):
        flashing_counter = 6
        while flashing_counter > 0:
            board, message_box = self.get_board(stdscr)
            board_string = build_sized_board_string(self.seriesmanager, game_won=True, flashing=flashing_counter % 2 == 0)
            board.addstr(board_string)
            self.center_lines_of_text(message_box, message_list)
            #stdscr.addstr(f"{self.seriesmanager.most_recent_game_winner()} wins! ")
            #stdscr.addstr(f"the score is now {self.seriesmanager.p1_score}-{self.seriesmanager.p2_score}\n")
            #stdscr.addstr("   press any key to play the next round.")
            board.refresh()
            time.sleep((0.25 if flashing_counter % 2 == 0 else 0.75))
            flashing_counter -= 1
        board.getch()


    def run_game_end_input(self, stdscr):
        stdscr.clear()
        messages = [f"{self.seriesmanager.most_recent_game_winner()} wins! ", f"the score is now {self.seriesmanager.p1_score}-{self.seriesmanager.p2_score}\n"]
        self.display_flashing_board(stdscr, messages)
       
        #stdscr.getch()
        self.seriesmanager.next_game()


    def run_match_end_input(self, stdscr):
        stdscr.clear()
        messages = [f"{self.seriesmanager.most_recent_game_winner()} wins the series! ", f"the final score is: {self.seriesmanager.p1_score}-{self.seriesmanager.p2_score}\n"]
        self.display_flashing_board(stdscr, messages)
        #stdscr.addstr(f"{self.seriesmanager.most_recent_game_winner()} wins the series! ")
        #stdscr.addstr(f"the final score is: {self.seriesmanager.p1_score}-{self.seriesmanager.p2_score}\n")
        #stdscr.addstr("press any key to return to home menu.")

        self.seriesmanager.play_another_match()
        
        
    def run_interface_screen(self, stdscr):
        stdscr.clear()
        stdscr.addstr(f"which interface would you like to use?\n[1] Simple\n[2] NCurses\n[3] GTK Gui\n[4] Quit")

        commandkey = self.get_valid_input(stdscr, interface_screen_options)

        #commandkey = stdscr.getkey()
        self.seriesmanager.interface_selected(commandkey)

    def select_change_name_screen(self, stdscr):
        stdscr.clear()
        stdscr.addstr(f"which player would you like to change the name for? [1/2]")
        is_valid, player_num = self.get_valid_input(stdscr, select_change_name_screen_options)
        if not is_valid:
            return
        stdscr.addstr(f"\nchanging name for {self.seriesmanager.p1_name if player_num == "1" else self.seriesmanager.p2_name}: ")
        player_num = True if player_num == "1" else False
        self.seriesmanager.select_player_name_change(player_num)


    def enter_change_name_screen(self, stdscr):
        stdscr.clear()
        stdscr.addstr(f"Changing name to: {self.seriesmanager.name_change_buffer}")
        #curses.echo()
        is_valid, next_char = self.get_valid_input(stdscr, enter_change_name_screen_options)
        if not is_valid:
            return
        elif next_char == 10:
            self.seriesmanager.enter_player_name_change()
        else:
            self.seriesmanager.add_letter_to_name_change_buffer(next_char)
        #new_name = stdscr.getstr().decode('utf-8')
        #curses.noecho()

        #self.seriesmanager.enter_player_name_change(new_name)


    def paint_ncurses_screen(self, stdscr):
       current_state = self.seriesmanager.current_state
       match current_state:
            case SeriesManager.menu_screen:
                self.run_menu_screen_input(stdscr)
            case SeriesManager.interface_screen:
                run_interface_screen(stdscr)
            case SeriesManager.select_change_name:
                select_change_name_screen(stdscr)
            case SeriesManager.enter_change_name:
                enter_change_name_screen(stdscr)
            case SeriesManager.p1_turn:
                self.run_player_turn(stdscr, 1)
            case SeriesManager.p2_turn:
                self.run_player_turn(stdscr, 2)
            case SeriesManager.game_end:
                self.run_game_end_input(stdscr)
            case SeriesManager.match_end:
                self.run_match_end_input(stdscr)



    def enter_ncurses_mode(self, stdscr):
        stdscr.keypad(True)
            
        while (self.seriesmanager.interface_mode == InterfaceMode.NCURSES):
            self.paint_ncurses_screen(stdscr)        



    def enter_ncurses_mode_wrapper(self):
        curses.wrapper(self.enter_ncurses_mode)
        
