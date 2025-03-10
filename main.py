
from enum import Enum

# game imports
from src.game.series_manager import SeriesManager, InterfaceMode

# interface imports
from src.interfaces.simple_terminal.simple_terminal_viewer import enter_simple_mode
from src.interfaces.ncursesterminal.ncurses_terminal_viewer import enter_ncurses_mode_wrapper

from src.interfaces.ncursesterminal.ncurses_printer import *

from src.logging.my_logging import logger

if __name__ == "__main__":


    seriesmanager = SeriesManager("scshafe", "yeet", InterfaceMode.NCURSES)

    # This is the home MENU loop
    while (seriesmanager.interface_mode != InterfaceMode.QUIT_GAME):
        logger.info(f"Entering game mode: {seriesmanager.interface_mode}")

        if (seriesmanager.interface_mode == InterfaceMode.SIMPLE):
            enter_simple_mode(seriesmanager)
        if (seriesmanager.interface_mode == InterfaceMode.NCURSES):
            enter_ncurses_mode_wrapper(seriesmanager)
        if (seriesmanager.interface_mode == InterfaceMode.GTK_GUI):
            logger.info("Sorry GTK not yet implemented")
            interface_mode = InterfaceMode.SIMPLE
        
    logger.info("Quitting Game")
    print("Thanks for playing!")