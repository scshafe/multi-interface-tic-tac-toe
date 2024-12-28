menu_string = """[M] to Open Menu"""
play_string = """[P] to Play Game"""
change_p_name_string = """[C] to Change a player's name"""
# change_p2_name_string = """[C2] to Change Player 2's name"""
end_game_string = """[E] to Exit Match"""
turn_string = """[Row,Col] to Make Move"""


run_menu_screen_input_string = """Welcome to Tic-Tac-Toe!
{play_string}
{change_p_name_string}

""".format(play_string=play_string, change_p_name_string=change_p_name_string)

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