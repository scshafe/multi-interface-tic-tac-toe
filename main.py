
from enum import Enum

# game imports
from src.game.series_manager import SeriesManager, InterfaceMode

# interface imports
from src.interfaces.simple_terminal.simple_terminal_viewer import enter_simple_mode
from src.interfaces.ncursesterminal.terminal_viewer import CursesGUI

from src.interfaces.ncursesterminal.printers import *

from src.logging.my_logging import logger

if __name__ == "__main__":


    seriesmanager = SeriesManager("scshafe", "yeet", InterfaceMode.NCURSES)

    # This is the home MENU loop
    while (seriesmanager.interface_mode != InterfaceMode.QUIT_GAME):
        logger.info(f"Entering game mode: {seriesmanager.interface_mode}")

        if (seriesmanager.interface_mode == InterfaceMode.SIMPLE):
            enter_simple_mode(seriesmanager)
        if (seriesmanager.interface_mode == InterfaceMode.NCURSES):
            curse_gui = CursesGUI(seriesmanager, size=3)
            curse_gui.enter_ncurses_mode_wrapper()
            #enter_ncurses_mode_wrapper(seriesmanager)
        if (seriesmanager.interface_mode == InterfaceMode.GTK_GUI):
            logger.info("Sorry GTK not yet implemented")
            interface_mode = InterfaceMode.SIMPLE
        
    logger.info("Quitting Game")
    print("Thanks for playing!")
