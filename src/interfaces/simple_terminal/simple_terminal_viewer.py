# 
from src.game.series_manager import SeriesManager
from src.interfaces.simple_terminal.simple_terminal_strings import *



def print_board(series_manager):
    s = series_manager.board
    print(board_string.format(a=s[0][0], b=s[0][1], c=s[0][2], d=s[1][0], e=s[1][1], f=s[1][2], g=s[2][0], h=s[2][1], i=s[2][2]))


def run_menu_screen_input(seriesmanager):
    command_input = input(run_menu_screen_input_string)

    match command_input:
        case "P":
            seriesmanager.play_game()
            print(seriesmanager.current_state)
        case "C":
            seriesmanager.change_names()
        case _:
            error_input_message()


def change_name_screen(seriesmanager):
    player_num = input("Which player would you like to change the name for? [1/2]")
    new_name = input("New player name: ")

    seriesmanager.change_new_name(player_num, new_name)



def valid_input_for_player_turn(command_input):
    if len(command_input) != 3:
        return False
    if not command_input[0].isnumeric() or not command_input[2].isnumeric():
        return False

    row = int(command_input[0])
    col = int(command_input[2])
    if row <= 2 and row >= 0 and col <= 2 and col >= 0:
        return True
    return False


def run_player_turn(seriesmanager, player_turn):
    print_board(seriesmanager)
    player_name = seriesmanager.current_player()
    command_input = input(f"It's {player_name}'s turn:")

    if valid_input_for_player_turn(command_input):
        seriesmanager.p_move(command_input)
    
    elif command_input == "M":
        seriesmanager.send("open_menu")


def run_game_end_input(seriesmanager):
    print("{} won the game. The score is now:\n\n".format(seriesmanager.most_recent_game_winner()))
    print("{}: {}".format(seriesmanager.p1_name, seriesmanager.p1_score))
    print("{}: {}".format(seriesmanager.p2_name, seriesmanager.p2_score))
    input("\nReady to play the next round? [Y]")

    seriesmanager.next_game()
    return

def run_match_end_input(seriesmanager):
    print("{} won the match. The final score is:\n\n".format(seriesmanager.most_recent_game_winner()))
    print("{}: {}".format(seriesmanager.p1_name, seriesmanager.p1_score))
    print("{}: {}".format(seriesmanager.p2_name, seriesmanager.p2_score))
    input("Press enter to return to home menu:")
    seriesmanager.play_another_match()



def enter_simple_mode(seriesmanager):

    while (True):
        current_state = seriesmanager.current_state

        match current_state:
            case SeriesManager.menu_screen:
                run_menu_screen_input(seriesmanager)
            case SeriesManager.change_name:
                change_name_screen(seriesmanager)
            case SeriesManager.p1_turn:
                run_player_turn(seriesmanager, 1)
            case SeriesManager.p2_turn:
                run_player_turn(seriesmanager, 2)
            case SeriesManager.game_end:
                run_game_end_input(seriesmanager)
            case SeriesManager.match_end:
                run_match_end_input(seriesmanager)
