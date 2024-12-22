# from ..game.gamestate import GameState
from statemachine import StateMachine, State
from enum import Enum

class InterfaceMode(Enum):
    QUIT_GAME = 1
    SIMPLE = 2
    NCURSES = 3
    GTK_GUI = 4


board_string = """
 {a} | {b} | {c}
   |   |
-----------
   |   |
 {d} | {e} | {f}
   |   |
-----------
   |   |
 {g} | {h} | {i}


"""

### State Machine:
# Menu
# X-turn
# O-turn
# Game-end - the end of 1 game in a multi-game series
# Match-end - the end of the full series


class SeriesManager(StateMachine):
    "A managing class for a series of individual games"

    menu_screen = State(initial=True)
    p1_turn = State()
    p2_turn = State()
    game_end = State()
    match_end = State()

    play_game = menu_screen.to(p1_turn)

    p_move = p1_turn.to(match_end, cond="match_winning_move") | p1_turn.to(game_end, cond="winning_move") | p1_turn.to(p2_turn, cond="valid_move") | p1_turn.to(p1_turn) | p2_turn.to(match_end, cond="match_winning_move") | p2_turn.to(game_end, cond="winning_move") | p2_turn.to(p1_turn, cond="valid_move") | p2_turn.to(p2_turn)
    # p_move = p2_turn.to(match_end, cond="match_winning_move") | p2_turn.to(game_end, cond="winning_move") | p2_turn.to(p2_turn, cond="valid_move") | p2_turn.to(p2_turn)

    open_menu = p1_turn.to(menu_screen) | p2_turn.to(menu_screen) | game_end.to(menu_screen)

    play_another_match = match_end.to(menu_screen)
    
    def current_player(self):
        return self.p1_name if self.current_state == SeriesManager.p1_turn else self.p2_name

    def __init__(self, p1_name="player 1", p2_name="player 2", interface_mode=InterfaceMode.SIMPLE):
        self.board = [[' ' for i in range(3)] for j in range(3)]
        print(self.board)
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.p1_score = 0
        self.p2_score = 0
        self.interface_mode = interface_mode
        # StateMachine.__init__(self, menu_screen()
        super(SeriesManager, self).__init__()
    
    def winning_move(self, move_input):
        return False
    
    def valid_move(self, move_input):
        row = int(move_input[0])
        col = int(move_input[2])

        if self.board[row][col] == ' ':
            return True
        
        print("Error: {} is an invalid move".format(move_input))
        return False

    def match_winning_move(self, move_input):
        return False

    
    def before_p_move(self, move_input):
        row = int(move_input[0])
        col = int(move_input[2])

        if self.board[row][col] == ' ':
            
            print(f"{self.current_player()} moved!")
            piece = 'X' if self.current_state == SeriesManager.p1_turn else 'O'
            self.board[row][col] = piece
            return True
        return False


    def print_board(self):
        s = self.board
        print(board_string.format(a=s[0][0], b=s[0][1], c=s[0][2], d=s[1][0], e=s[1][1], f=s[1][2], g=s[2][0], h=s[2][1], i=s[2][2]))
    
        


