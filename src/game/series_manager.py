from src.game.gamestate import *
from statemachine import StateMachine, State
from enum import Enum
from copy import deepcopy

class InterfaceMode(Enum):
    QUIT_GAME = 1
    SIMPLE = 2
    NCURSES = 3
    GTK_GUI = 4



### State Machine:
# Menu
# X-turn
# O-turn
# Game-end - the end of 1 game in a multi-game series
# Match-end - the end of the full series



class SeriesManager(StateMachine):
    "A managing class for a series of individual games"

    menu_screen = State(initial=True)
    change_name = State()
    p1_turn = State()
    p2_turn = State()
    game_end = State()
    match_end = State()

    change_names = menu_screen.to(change_name)
    change_new_name = change_name.to(menu_screen)
    play_game = menu_screen.to(p1_turn)

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
        return 'X' if self.current_state == SeriesManager.p1_turn else 'O'
    
    def current_player(self):
        return self.p1_name if self.current_state == SeriesManager.p1_turn else self.p2_name

    def __init__(self, p1_name="player 1", p2_name="player 2", interface_mode=InterfaceMode.SIMPLE):
        self.board = create_new_board()
        print(self.board)
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.p1_score = 0
        self.p2_score = 0
        self.play_to_total = 2
        self.interface_mode = interface_mode
        self.game_log = list()
        # StateMachine.__init__(self, menu_screen()
        super(SeriesManager, self).__init__()
    
    def winning_move(self, move_input):
        print("winning_move() called")
        temp_board = deepcopy(self.board)
        row = int(move_input[0])
        col = int(move_input[2])
        temp_board[row][col] = self.current_player_piece()

        if not board_contains_3_in_a_row(temp_board):
            return False
        return True
    
    def on_enter_game_end(self):
        print("on_enter_game_end() called")
        # a player did win
        temp_board = deepcopy(self.board)
        if board_contains_3_in_a_row_for_piece(temp_board, 'X'):
            self.p1_score += 1
            self.game_log.append('X')
        else:
            self.p2_score += 1
            self.game_log.append('O')
    
    def on_exit_game_end(self):
        self.board = create_new_board()
    
    def most_recent_game_winner(self):
        return self.p1_name if self.game_log[-1] == 'X' else self.p2_name

    def valid_move(self, move_input):
        print("valid_move() called")
        print(self.board)
        row = int(move_input[0])
        col = int(move_input[2])

        if self.board[row][col] == ' ':
            return True
        
        print("Error: {} is an invalid move".format(move_input))
        return False

    def match_winning_move(self, move_input):
        print("match_winning_move() called")
        if self.current_state == SeriesManager.p1_turn and self.p1_score + 1 == self.play_to_total:
            return True
        if self.current_state == SeriesManager.p2_turn and self.p2_score + 1 == self.play_to_total:
            return True
        return False

    def on_enter_match_end(self):
        print("on_enter_match_end() called")
        temp_board = deepcopy(self.board)
        if board_contains_3_in_a_row_for_piece(temp_board, 'X'):
            self.p1_score += 1
            self.game_log.append('X')
        else:
            self.p2_score += 1
            self.game_log.append('O')

    
    def on_p_move(self, move_input):
        print("before_p_move() called")
        row = int(move_input[0])
        col = int(move_input[2])

        if self.board[row][col] == ' ':
            
            print(f"{self.current_player()} moved!")
            piece = self.current_player_piece()
            self.board[row][col] = piece
            return True
        return False

    def on_change_new_name(self, player_num, new_player_name):
        if player_num != '1' and player_num != '2':
            print("Error: player number must be 1 or 2")
            return False
        
        if player_num == '1':
            self.p1_name = new_player_name
        else:
            self.p2_name = new_player_name
        return True

    def p1_goes_first(self):
        return True
    
        


