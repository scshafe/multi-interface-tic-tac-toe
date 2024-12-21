
from enum import Enum

# game imports
from src.game.series_manager import SeriesManager, InterfaceMode

# interface imports
from src.interfaces.simple_terminal.simple_terminal_viewer import enter_simple_mode



if __name__ == "__main__":


    seriesmanager = SeriesManager()
    print(seriesmanager.current_state)

    input("here")


    # This is the home MENU loop
    while (interface_mode != InterfaceMode.QUIT_GAME):

        if (interface_mode == InterfaceMode.SIMPLE):
            # Await command
            enter_simple_mode(seriesmanager)

        if (interface_mode == InterfaceMode.NCURSES):
            print("Ncurses Game Mode")

            enter_ncurses_mode(seriesmanager)
        
        if (interface_mode == InterfaceMode.GTK_GUI):
            print("Sorry GTK not yet implemented")
            interface_mode = InterfaceMode.SIMPLE
            # start GUI
        
        input("next line")