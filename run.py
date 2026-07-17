import curses
import db

from interface.home import HomeScreen
from interface.session import SessionScreen
from interface.statistics import StatisticsScreen

def main(stdscr: curses.window) -> None:
    """ RENDERS THE TUI """
    height, width = stdscr.getmaxyx()
    height_center = (height // 2)
    width_center = (width // 2)

    connection = db.get_connection()
    db.initialize_db(connection)

    while True:
        choice = HomeScreen(stdscr=stdscr, height_center=height_center, width_center=width_center)

        if choice == 0:
            SessionScreen(stdscr=stdscr, height_center=height_center, width_center=width_center, connection=connection)
        elif choice == 1:
            StatisticsScreen(stdscr=stdscr, height_center=height_center, width_center=width_center, connection=connection)
        elif choice == 2:
            break

def main_wrapper():
    curses.wrapper(main)
