from src.game.gamestate import *
from statemachine import StateMachine, State
from enum import Enum
from copy import deepcopy
from random import randint

import curses

from src.logging.my_logging import logger

class InterfaceMode(Enum):
    SIMPLE = 1
    NCURSES = 2
    GTK_GUI = 3
    QUIT_GAME = 4


class SelectedTileDirections(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    INVALID = 5



class SeriesManager(StateMachine):
    "A managing class for a series of individual games"

    menu_screen = State(initial=True)
    interface_screen = State()
    select_change_name = State()
    enter_change_name = State()
    p1_turn = State()
    p2_turn = State()
    game_end = State()
    match_end = State()

    change_interface = menu_screen.to(interface_screen)
    quit_game = menu_screen.to(menu_screen)
    interface_selected = interface_screen.to(menu_screen)

    change_player_name = menu_screen.to(select_change_name)
    select_player_name_change = select_change_name.to(enter_change_name)
    enter_player_name_change = enter_change_name.to(menu_screen)
    play_game = menu_screen.to(p1_turn)

    p_change_tile = p1_turn.to(p1_turn) | p2_turn.to(p2_turn)

    p_move = p1_turn.to(match_end, cond=["valid_move", "winning_move", "match_winning_move"]) |  \
             p1_turn.to(game_end, cond=["valid_move", "winning_move"]) | \
             p1_turn.to(p2_turn, cond="valid_move") | \
             p1_turn.to(p1_turn) | \
             p2_turn.to(match_end, cond=["valid_move", "winning_move", "match_winning_move"]) |  \
             p2_turn.to(game_end, cond=["valid_move", "winning_move"]) | \
             p2_turn.to(p1_turn, cond="valid_move") | \
             p2_turn.to(p2_turn)

    open_menu = p1_turn.to(menu_screen) | \
                p2_turn.to(menu_screen) | \
                game_end.to(menu_screen)
    
    # add logic here to determine who should play first next game (in )
    next_game = game_end.to(p1_turn, cond="p1_goes_first") | \
                game_end.to(p2_turn)

    play_another_match = match_end.to(menu_screen)

    def current_player_piece(self):
        return Tile.P1 if self.current_state == SeriesManager.p1_turn else Tile.P2
    
    def current_player(self):
        return self.p1_name if self.current_state == SeriesManager.p1_turn else self.p2_name

    def __init__(self, p1_name="player 1", p2_name="player 2", interface_mode=InterfaceMode.SIMPLE):
        self.board = create_new_board()
        self.selected_tile_map = [[False for i in range(3)] for j in range(3)] # selected tile map is for ncurses and gtk guis (highlights the currently selected square)
        self.selected_tile_map[0][0] = True
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.name_change_buffer = ""
        self.p1_score = 0
        self.p2_score = 0
        self.play_to_total = 2
        self.interface_mode = interface_mode
        self.game_log = list()
        super(SeriesManager, self).__init__()
    
    def winning_move(self, move_input):
        logger.info("entering winning_move")
        row,col = None, None
        if self.interface_mode == InterfaceMode.NCURSES:
            row,col = self.find_selected_tile()
        elif self.interface_mode == InterfaceMode.SIMPLE:
            row = int(move_input[0])
            col = int(move_input[2])
        temp_board = deepcopy(self.board)
        temp_board[row][col] = self.current_player_piece()

        if not board_contains_3_in_a_row(temp_board):
            return False
        self.win = board_contains_3_in_a_row(temp_board)
        return True
    
    def on_enter_game_end(self):
        # a player did win
        logger.info("entering on_eneter_game_end")
        temp_board = deepcopy(self.board)
        if board_contains_3_in_a_row_for_piece(temp_board, Tile.P1):
            self.p1_score += 1
            self.game_log.append(Tile.P1)
        else:
            self.p2_score += 1
            self.game_log.append(Tile.P2)
    
    def on_exit_game_end(self):
        logger.info("entering on_exit_game_end")
        self.board = create_new_board()
    
    def most_recent_game_winner(self):
        if len(self.game_log) == 0:
            return ""
        return self.p1_name if self.game_log[-1] == Tile.P1 else self.p2_name

    def valid_move(self, move_input):
        logger.info(f"entering valid_move: {move_input}")
        if self.interface_mode == InterfaceMode.NCURSES:
            logger.info("valid move")
            row,col = self.find_selected_tile()
            if self.board[row][col] == Tile.BLANK:
                logger.info("valid move true")
                return True
            return False

        row = int(move_input[0])
        col = int(move_input[2])

        if self.board[row][col] == Tile.BLANK:
            return True
        
        logger.error("Error: {} is an invalid move".format(move_input))
        return False

    def match_winning_move(self):
        # if self.interface_mode == InterfaceMode.NCURSES:
        #     return False
        if self.current_state == SeriesManager.p1_turn and self.p1_score + 1 == self.play_to_total:
            return True
        if self.current_state == SeriesManager.p2_turn and self.p2_score + 1 == self.play_to_total:
            return True
        return False

    def on_enter_match_end(self):
        temp_board = deepcopy(self.board)
        if board_contains_3_in_a_row_for_piece(temp_board, Tile.P1):
            self.p1_score += 1
            self.game_log.append(Tile.P1)
        else:
            self.p2_score += 1
            self.game_log.append(Tile.P1)

    
    def on_p_move(self, move_input):
        logger.info(f"entering on_p_move: {move_input}")
        if self.interface_mode == InterfaceMode.NCURSES:
            row,col = self.find_selected_tile()
            if self.board[row][col] != Tile.BLANK:
                logger.info("player attempted to move at occupied square")
                return False
            logger.info(f"player moved at: {row},{col}")
            self.board[row][col] = self.current_player_piece()
            return True
        elif self.interface_mode == InterfaceMode.SIMPLE:
            row = int(move_input[0])
            col = int(move_input[2])

            if self.board[row][col] == Tile.BLANK:
                
                logger.info(f"{self.current_player()} moved!")
                piece = self.current_player_piece()
                self.board[row][col] = piece
                return True
            return False

    def on_select_player_name_change(self, player_num):
        # should be True for player 1, False for player 2 
        if player_num != True and player_num != False:
            logger.error(f"Error: incorrect player_num entered: {player_num}")
        self.player_name_change = player_num

    def add_letter_to_name_change_buffer(self, next_char):
        self.name_change_buffer = self.name_change_buffer + next_char

    def on_enter_player_name_change(self):
        old_name = self.p1_name if self.player_name_change else self.p2_name
        player_num = 1 if self.player_name_change else 2
        logger.info(f"changing name for player_num: {player_num} from {old_name} to {self.name_change_buffer}")
        
        if self.player_name_change:
            self.p1_name = self.name_change_buffer
        else:
            self.p2_name = self.name_change_buffer
        self.name_change_buffer = ""
        return True

    def p1_goes_first(self):
        return True if randint(1,2) == 1 else False
    
    def on_interface_selected(self, interface_input):

        # Error check to make sure it is int here
        self.interface_mode = InterfaceMode(int(interface_input))
    
    def on_quit_game(self):
        self.interface_mode = InterfaceMode.QUIT_GAME
    

    def on_p_change_tile(self, direction):
        
        logger.info("entering on_p_change_tile")
        for row in range(len(self.selected_tile_map)):
            for col in range(len(self.selected_tile_map[0])):
                if self.selected_tile_map[row][col]:
                    self.selected_tile_map[row][col] = False
                    
                    if direction == SelectedTileDirections.UP:
                        self.selected_tile_map[(row-1)%3][col] = True
                    elif direction == SelectedTileDirections.RIGHT:
                        self.selected_tile_map[row][(col+1)%3] = True
                    elif direction == SelectedTileDirections.DOWN:
                        self.selected_tile_map[(row+1)%3][col] = True
                    elif direction == SelectedTileDirections.LEFT:
                        self.selected_tile_map[row][(col-1)%3] = True
                    else:
                        logger.info("ERROR: invalid direction entered into on_p_change_tile")
                    return
        
    def find_selected_tile(self):
        for row in range(3):
            for col in range(3):
                if self.selected_tile_map[row][col]:
                    return row,col
