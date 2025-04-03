import curses




def menu_screen_validator(key):
    return chr(key) == "p" or chr(key) == "c" or chr(key) == "i" or chr(key) == "q"


run_player_turn_set = {curses.KEY_UP, curses.KEY_RIGHT, curses.KEY_DOWN, curses.KEY_LEFT, 10, "m"} 
def run_player_turn_validator(key):
    return key in run_player_turn_set


