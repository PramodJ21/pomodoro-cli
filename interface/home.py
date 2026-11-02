import curses
import sqlite3
import db
from interface.animations import (
    get_next_theme,
    get_theme_display_name,
)


def HomeScreen(
    stdscr: curses.window,
    height_center: int,
    width_center: int,
    connection: sqlite3.Connection | None = None,
) -> int:
    title = r"""
    ____   ___  __  __  ___  ____   ___  ____   ___
   |  _ \ / _ \|  \/  |/ _ \|  _ \ / _ \|  _ \ / _ \
   | |_) | | | | |\/| | | | | | | | | | | |_) | | | |
   |  __/| |_| | |  | | |_| | |_| | |_| |  _ <| |_| |
   |_|    \___/|_|  |_|\___/|____/ \___/|_| \_\\___/
    """
    selected = 0
    current_theme = db.get_setting(connection, "theme", "bonfire") if connection else "bonfire"

    while True:
        theme_display = get_theme_display_name(current_theme)
        options = [
            "Start Session",
            "Show Statistics",
            f"Theme: {theme_display}",
            "Exit",
        ]
        no_of_options = len(options)

        stdscr.clear()
        split_title = [l for l in title.splitlines() if l.strip()]
        row = max(1, height_center - len(split_title) - 3)
        for line in split_title:
            column = width_center - len(line) // 2
            try:
                stdscr.addstr(row, column, line)
            except curses.error:
                pass
            row += 1

        try:
            stdscr.addstr(row + 1, width_center - 14, "─" * 28)
        except curses.error:
            pass

        menu_row = row + 2
        for selection in range(no_of_options):
            r = menu_row + selection
            label = f"  {options[selection]}  "
            column = width_center - len(label) // 2
            attr = curses.A_REVERSE | curses.A_BOLD if selected == selection else 0
            try:
                if attr:
                    stdscr.addstr(r, column, label, attr)
                else:
                    stdscr.addstr(r, column, label)
            except curses.error:
                pass

        try:
            stdscr.addstr(menu_row + no_of_options + 1, width_center - 14, "─" * 28)
            hint = "↑↓ navigate   enter select   t theme"
            stdscr.addstr(menu_row + no_of_options + 2, width_center - len(hint) // 2, hint)
        except curses.error:
            pass

        stdscr.refresh()
        key = stdscr.getch()

        if key in (curses.KEY_UP, ord("k"), ord("K")):
            selected = (selected - 1) % no_of_options
        elif key in (curses.KEY_DOWN, ord("j"), ord("J")):
            selected = (selected + 1) % no_of_options
        elif key in (ord("t"), ord("T"), 9):
            current_theme = get_next_theme(current_theme)
            if connection:
                db.set_setting(connection, "theme", current_theme)
        elif key in (ord("\n"), curses.KEY_ENTER, ord("\r")):
            if selected == 0:
                return 0
            elif selected == 1:
                return 1
            elif selected == 2:
                # Cycle theme in-place
                current_theme = get_next_theme(current_theme)
                if connection:
                    db.set_setting(connection, "theme", current_theme)
            elif selected == 3:
                return 2  # Break/Exit code for run.py
