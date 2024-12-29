menu_string = """[M] to Open Menu"""
play_string = """[P] to Play Game"""
interface_string = """[I] to Change Interface"""
change_p_name_string = """[C] to Change a player's name"""
# change_p2_name_string = """[C2] to Change Player 2's name"""
end_game_string = """[E] to Exit Match"""
turn_string = """[Row,Col] to Make Move"""


run_menu_screen_input_string = """Welcome to Tic-Tac-Toe!
{play_string}
{change_p_name_string}
{interface_string}

""".format(play_string=play_string,
           change_p_name_string=change_p_name_string, 
           interface_string=interface_string)


run_interface_screen_input_string= """Which interface would you like to use?
[1] - Simple Terminal
[2] - NCurses Terminal
[3] - GTK Gui
[4] - Quit Game
"""

run_p1_turn_string = """
{turn_string}
{menu_string}
""".format(turn_string=turn_string, menu_string=menu_string)


def error_input_message():
    print("Sorry, your input is either invalid or not yet implemented. Please try again.")


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