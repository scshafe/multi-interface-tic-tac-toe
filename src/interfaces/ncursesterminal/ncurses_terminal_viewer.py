
import curses








def enter_ncurses_mode(stdscr, seriesmanager):

    # ~~~~~~~~~~~~~~~~~~~~ SETUP NCURSES MODE ~~~~~~~~~~~~~~~~~~~

    # stdscr = curses.initscr()

    # turns off automatic ehcoing of keys to the screen
    # curses.noecho()

    # react to keys instantly, without require the [Enter] key to be pressed
    # curses.cbreak()

    # return special value such as `curses.KEY_LEFT` intead of multibyte escape sequence
    # curses.keypad(True)
    curses.echo()

    stdscr.clear()

    stdscr.addstr("Pretty text")
    stdscr.refresh()

    # print("Entered ncurses mode: ", seriesmanager.interface_mode)
    # print(f"curses size: {curses.LINES} rows, {curses.COLS} cols")
    
    stdscr.refresh()
    
    while True:
        c = stdscr.getch()
        if c == ord('m'):
            stdscr.addstr("m detected")

    # ~~~~~~~~~~~~~~~~~~~~ MAIN EXECUTION LOOP ~~~~~~~~~~~~~~~~~~

    # stdscr.addstr("curses mode activated")
    # stdscr.refresh()

    # ~~~~~~~~~~~~~~~~~~~~ EXIT NCURSES MODE ~~~~~~~~~~~~~~~~~~~
    # curses.nocbreak()
    # stdscr.keypad(False)
    # curses.echo()



def enter_ncurses_mode_wrapper(seriesmanager):
    curses.wrapper(enter_ncurses_mode, seriesmanager)