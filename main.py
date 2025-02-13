
from enum import Enum

# game imports
from src.game.series_manager import SeriesManager, InterfaceMode

# interface imports
from src.interfaces.simple_terminal.simple_terminal_viewer import enter_simple_mode
from src.interfaces.ncursesterminal.ncurses_terminal_viewer import enter_ncurses_mode_wrapper

from src.interfaces.ncursesterminal.ncurses_printer import *

from src.logging.my_logging import logger

if __name__ == "__main__":

    
    logger.info("yeet2")

    seriesmanager = SeriesManager("scshafe", "yeet", InterfaceMode.NCURSES)

    # print(build_board_string(seriesmanager))
    # input()

    # This is the home MENU loop
    while (seriesmanager.interface_mode != InterfaceMode.QUIT_GAME):

        if (seriesmanager.interface_mode == InterfaceMode.SIMPLE):
            # Await command
            enter_simple_mode(seriesmanager)

        if (seriesmanager.interface_mode == InterfaceMode.NCURSES):
            print("Ncurses Game Mode")

            enter_ncurses_mode_wrapper(seriesmanager)
        
        if (seriesmanager.interface_mode == InterfaceMode.GTK_GUI):
            print("Sorry GTK not yet implemented")
            interface_mode = InterfaceMode.SIMPLE
            # start GUI
        
    print("Quitting Game")