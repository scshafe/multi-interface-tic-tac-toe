# from ..game.gamestate import GameState
from statemachine import StateMachine, State
from enum import Enum

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

def board_contains_3_in_a_row(board):
    for row in range(3):
        if board[row][0] == board[row][1] and board[row][1] == board[row][2]:
            return True
    for col in range(3):
        if board[0][col] == board[1][col] and board[1][col] == board[2][col]:
            return True
    
    # diagonals
    if board[0][0] == board[1][1] and board [1][1] == board[2][2]:
        return True
    if board[2][0] == board[1][1] and board [1][1] == board[0][2]:
        return True
    return False


def create_new_board():
    return [[' ' for i in range(3)] for j in range(3)]

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
        self.interface_mode = interface_mode
        # StateMachine.__init__(self, menu_screen()
        super(SeriesManager, self).__init__()
    
    def winning_move(self, move_input):
        temp_board = self.board
        row = int(move_input[0])
        col = int(move_input[2])
        temp_board[row][col] = self.current_player_piece()

        if board_contains_3_in_a_row(temp_board):
            return True
        return False
    
    def valid_move(self, move_input):
        print("valid_move called")
        row = int(move_input[0])
        col = int(move_input[2])

        if self.board[row][col] == ' ':
            return True
        
        print("Error: {} is an invalid move".format(move_input))
        return False

    def match_winning_move(self, move_input):
        return False

    
    def before_p_move(self, move_input):
        print("before_p_move called")
        row = int(move_input[0])
        col = int(move_input[2])

        if self.board[row][col] == ' ':
            
            print(f"{self.current_player()} moved!")
            piece = self.current_player_piece()
            self.board[row][col] = piece
            return True
        return False

    def before_change_new_name(self, player_num, new_player_name):
        if player_num != '1' and player_num != '2':
            print("Error: player number must be 1 or 2")
            return False
        
        if player_num == '1':
            self.p1_name = new_player_name
        else:
            self.p2_name = new_player_name
        return True

    
    
        


