import curses




def menu_screen_validator(key):
    return key == "p" or key == "c" or key == "i" or key == "q"


run_player_turn_set = {curses.KEY_UP, curses.KEY_RIGHT, curses.KEY_DOWN, curses.KEY_LEFT, 10, "m"} 
def run_player_turn_validator(key):
    return key in run_player_turn_set


