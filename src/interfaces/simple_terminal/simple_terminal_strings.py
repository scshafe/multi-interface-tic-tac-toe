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


def run_game_end_input_string(seriesmanager):
  return """
{match_winner} won the game. The score is:

{p1_name}: {p1_score}
{p2_name}: {p2_score}

Series is first to {series_score}
Press [enter] to begin next game.
""".format(match_winner=seriesmanager.most_recent_game_winner(),
          p1_name=seriesmanager.p1_name,
          p1_score=seriesmanager.p1_score,
          p2_name=seriesmanager.p2_name,
          p2_score=seriesmanager.p2_score,
          series_score=seriesmanager.play_to_total)


def run_match_end_input_string(seriesmanager):
    return """
{match_winner} won the match. The final score is:

{p1_name}: {p1_score}
{p2_name}: {p2_score}

Press [enter] to return to home menu.
""".format(match_winner=seriesmanager.most_recent_game_winner(),
          p1_name=seriesmanager.p1_name,
          p1_score=seriesmanager.p1_score,
          p2_name=seriesmanager.p2_name,
          p2_score=seriesmanager.p2_score)



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