
from src.game.series_manager import SeriesManager

menu_string = """[M] to Open Menu"""
play_string = """[P] to Play Game"""
change_p1_name_string = """[C1] to Change Player 1's name"""
change_p2_name_string = """[C2] to Change Player 2's name"""
end_game_string = """[E] to Exit Match"""
turn_string = """[Row,Col] to Make Move"""


def error_input_message():
    print("Sorry, your input is either invalid or not yet implemented. Please try again.")




def run_menu_screen_input(seriesmanager):
    command_input = input(f"Welcome to Tic-Tac-Toe! Would you like to:\n{play_string}\n{change_p1_name_string}\n{change_p2_name_string}")

    match command_input:
        case "P":
            seriesmanager.play_game
        case _:
            error_input_message()


def run_p1_turn(seriesmanager):
    input(f"It's {seriesmanager.p1_name}'s turn:")

def run_o_turn(seriesmanager):
    return

def run_game_end_input(seriesmanager):
    return

def run_match_end_input(seriesmanager):
    return

def enter_simple_mode(seriesmanager):

    while (True):
        current_state = seriesmanager.current_state

        match current_state:
            case SeriesManager.menu_screen:
                run_menu_screen_input(seriesmanager)
            case SeriesManager.p1_turn:
                run_p1_turn(seriesmanager)
            case SeriesManager.p2_turn:
                print("p2 turn")
            case SeriesManager.game_end:
                print("game end")
            case SeriesManager.match_end:
                print("match end")
