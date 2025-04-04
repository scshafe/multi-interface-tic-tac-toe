import curses


menu_screen_options = {"p", "c", "i", "q"}

run_player_turn_options = {curses.KEY_UP, curses.KEY_RIGHT, curses.KEY_DOWN, curses.KEY_LEFT, 10, "m"} 

interface_screen_options = {1 , 2, 3, 4}


def validator(key, input_options):
    return key in input_options
