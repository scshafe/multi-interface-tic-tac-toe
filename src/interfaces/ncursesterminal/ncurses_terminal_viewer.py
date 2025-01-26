
import curses

def enter_ncurses_mode(seriesmanager):


    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.clear()

    stdscr.addstr("Pretty text", curses.color_pair(1))
    stdscr.refresh()

    print("Entered ncurses mode: ", seriesmanager.interface_mode)
    input("Need to implement")


