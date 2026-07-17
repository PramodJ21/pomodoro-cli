import curses
def HomeScreen(
    stdscr: curses.window,
    height_center: int,
    width_center: int
    ):
    no_of_options = 3
    options = ["Start Session", "Show Statistics", "Exit"]
    title = r"""
    ____   ___  __  __  ___  ____   ___  ____   ___
   |  _ \ / _ \|  \/  |/ _ \|  _ \ / _ \|  _ \ / _ \
   | |_) | | | | |\/| | | | | | | | | | | |_) | | | |
   |  __/| |_| | |  | | |_| | |_| | |_| |  _ <| |_| |
   |_|    \___/|_|  |_|\___/|____/ \___/|_| \_\\___/
    """
    selected = 0
    while True:
        stdscr.clear()
        row = height_center - len(title.splitlines())
        column = width_center - len(title.splitlines()[2]) // 2
        for line in title.splitlines():
            stdscr.addstr(row, column, line)
            row += 1

        stdscr.addstr(height_center, width_center - 12, "─" * 24)

        for selection in range(no_of_options):
            row = height_center + (selection + 1)
            label = f"  {options[selection]}  "
            column = width_center - len(label) // 2
            if selected == selection:
                stdscr.addstr(row, column, label, curses.A_REVERSE | curses.A_BOLD)
            else:
                stdscr.addstr(row, column, label)

        stdscr.addstr(height_center + no_of_options + 1, width_center - 12, "─" * 24)
        hint = "↑↓ navigate   enter select"
        stdscr.addstr(height_center + no_of_options + 2, width_center - len(hint) // 2, hint)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % no_of_options
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % no_of_options
        elif key == ord("\n"):
            return selected
