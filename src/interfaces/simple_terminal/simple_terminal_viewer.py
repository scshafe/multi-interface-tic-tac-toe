# 
from src.game.series_manager import SeriesManager

menu_string = """[M] to Open Menu"""
play_string = """[P] to Play Game"""
change_p1_name_string = """[C1] to Change Player 1's name"""
change_p2_name_string = """[C2] to Change Player 2's name"""
end_game_string = """[E] to Exit Match"""
turn_string = """[Row,Col] to Make Move"""


run_menu_screen_input_string = """Welcome to Tic-Tac-Toe!
{play_string}
{change_p1_name_string}
{change_p2_name_string}
""".format(play_string=play_string, change_p1_name_string=change_p1_name_string, change_p2_name_string=change_p2_name_string)

run_p1_turn_string = """
{turn_string}
{menu_string}
""".format(turn_string=turn_string, menu_string=menu_string)


def error_input_message():
    print("Sorry, your input is either invalid or not yet implemented. Please try again.")




def run_menu_screen_input(seriesmanager):
    command_input = input(run_menu_screen_input_string)

    match command_input:
        case "P":
            seriesmanager.play_game()
            print(seriesmanager.current_state)
        case _:
            error_input_message()

def valid_input_for_player_turn(command_input):
    if len(command_input) != 3:
        return False
    if not command_input[0].isnumeric() or not command_input[2].isnumeric():
        return False

    row = int(command_input[0])
    col = int(command_input[2])
    if row <= 3 and row >= 1 and col <= 3 and col >= 1:
        return True
    return False


def run_p1_turn(seriesmanager):
    command_input = input(f"It's {seriesmanager.p1_name}'s turn:")

    if valid_input_for_player_turn(command_input):
        seriesmanager.p1_move(command_input)
    
    elif command_input == "M":
        seriesmanager.send("open_menu")

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
