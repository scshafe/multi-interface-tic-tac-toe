
import curses








def enter_ncurses_mode(seriesmanager):

    # ~~~~~~~~~~~~~~~~~~~~ SETUP NCURSES MODE ~~~~~~~~~~~~~~~~~~~

    stdscr = curses.initscr()

    # turns off automatic ehcoing of keys to the screen
    curses.noecho()

    # react to keys instantly, without require the [Enter] key to be pressed
    curses.cbreak()

    # return special value such as `curses.KEY_LEFT` intead of multibyte escape sequence
    curses.keypad(True)


    stdscr.clear()

    stdscr.addstr("Pretty text", curses.color_pair(1))
    stdscr.refresh()

    print("Entered ncurses mode: ", seriesmanager.interface_mode)
    input("Need to implement")

    # ~~~~~~~~~~~~~~~~~~~~ MAIN EXECUTION LOOP ~~~~~~~~~~~~~~~~~~



    # ~~~~~~~~~~~~~~~~~~~~ EXIT NCURSES MODE ~~~~~~~~~~~~~~~~~~~
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()



def enter_ncurses_mode_wrapper(seriesmanager):
    curses.wrapper(enter_ncurses_mode, seriesmanager)