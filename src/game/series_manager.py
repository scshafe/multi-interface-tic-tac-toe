from gamestate import GameState
from statemachine import StateMachine, State

class GameMode(Enum):
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
    menu_screen = State()
    x_turn = State()
    o_turn = State()
    game_end = State()
    match_end = State()

    play_game = menu_screen.to.x_turn()

    x_move = x_turn.to(game_end, conditions="winning_move") | x_turn.to(o_turn, conditions="valid_move") | x_turn.to(x_turn)
    o_move = o_turn.to(game_end, conditions="winning_move") | o_turn.to(o_turn, conditions="valid_move") | o_turn.to(o_turn)

    open_menu = x_turn.to(menu_screen) | o_turn.to(menu_screen) | game_end.to(menu_screen)

    match_over = match_end.to(menu_screen)
    


    def __init__(self, p1_name="player 1", p2_name="player 2", game_mode=GameMode.SIMPLE, game_state=GameState()):
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.p1_score = 0
        self.p2_score = 0
        self.game_mode = game_mode
        self.game_state = game_state
    



