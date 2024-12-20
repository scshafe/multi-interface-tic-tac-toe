
from enum import Enum

# game imports
from game.series_manager import SeriesManager, GameMode

# interface imports
from simple_terminal_viewer import enter_simple_mode



if __name__ == "__main__":

    seriesmanager = SeriesManager("scshafe", "opponent")

    game_mode = GameMode.SIMPLE


    # This is the home MENU loop
    while (game_mode != GameMode.QUIT_GAME):

        if (game_mode == GameMode.SIMPLE):
            # Await command
            enter_simple_mode(seriesmanager)

        if (game_mode == GameMode.NCURSES):
            print("Ncurses Game Mode")

            enter_ncurses_mode(seriesmanager)
        
        if (game_mode == GameMode.GTK_GUI):

            # start GUI
        
        input("next line")