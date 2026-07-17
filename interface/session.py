import curses
from datetime import datetime
import sqlite3
import session as sess

# ASCII digit segments — each digit is 5 lines tall
_DIGITS = {
    "0": ["█████", "█   █", "█   █", "█   █", "█████"],
    "1": ["  █  ", "  █  ", "  █  ", "  █  ", "  █  "],
    "2": ["█████", "    █", "█████", "█    ", "█████"],
    "3": ["█████", "    █", "█████", "    █", "█████"],
    "4": ["█   █", "█   █", "█████", "    █", "    █"],
    "5": ["█████", "█    ", "█████", "    █", "█████"],
    "6": ["█████", "█    ", "█████", "█   █", "█████"],
    "7": ["█████", "    █", "    █", "    █", "    █"],
    "8": ["█████", "█   █", "█████", "█   █", "█████"],
    "9": ["█████", "█   █", "█████", "    █", "█████"],
    ":": ["     ", "  █  ", "     ", "  █  ", "     "],
}

def _render_big_time(stdscr: curses.window, row: int, width_center: int, time_str: str, attr: int = 0):
    chars = list(time_str)
    total_width = len(chars) * 6 - 1
    col_start = width_center - total_width // 2

    for line_idx in range(5):
        col = col_start
        for ch in chars:
            segment = _DIGITS.get(ch, ["     "] * 5)[line_idx]
            stdscr.addstr(row + line_idx, col, segment, attr)
            col += 6


def _draw_progress_bar(stdscr: curses.window, row: int, width_center: int, elapsed: int, total: int, width: int = 40):
    filled = int((elapsed / total) * width) if total > 0 else 0
    filled = min(filled, width)
    bar = "█" * filled + "░" * (width - filled)
    col = width_center - width // 2
    stdscr.addstr(row, col, bar)


def SessionScreen(
    stdscr: curses.window,
    height_center: int,
    width_center: int,
    connection: sqlite3.Connection
):
    session_times = [(25*60, 5*60), (50 * 60, 10 * 60), (75 * 60, 15 * 60), (110 * 60, 20 * 60)]
    labels = ["  25 min / 5 min break  ", "  50 min / 10 min break  ", "  75 min / 15 min break  ", "  110 min / 20 min break  ", "  Back  "]
    selected = 0
    title = r"""
    ____  _____ ____ ____ ___ ___  _   _
   / ___|| ____/ ___/ ___|_ _/ _ \| \ | |
   \___ \|  _| \___ \___ \| | | | |  \| |
    ___) | |___ ___) |__) | | |_| | |\  |
   |____/|_____|____/____/___\___/|_| \_|
    """

    while True:
        stdscr.clear()
        split_title = title.splitlines()
        row = height_center - len(split_title) - 2
        column = width_center - len(split_title[2]) // 2
        for line in split_title:
            stdscr.addstr(row, column, line)
            row += 1

        stdscr.addstr(height_center, width_center - 12, "─" * 24)

        for i, label in enumerate(labels):
            r = height_center + (i + 1)
            c = width_center - len(label) // 2
            if selected == i:
                stdscr.addstr(r, c, label, curses.A_REVERSE | curses.A_BOLD)
            else:
                stdscr.addstr(r, c, label)

        stdscr.addstr(height_center + len(labels) + 1, width_center - 12, "─" * 24)
        stdscr.addstr(height_center + len(labels) + 2, width_center - 14, "↑↓ navigate   enter select")

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(labels)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(labels)
        elif key == ord("\n"):
            if selected == len(labels) - 1:
                break
            else:
                work_duration, break_duration = session_times[selected]
                _run_timer(stdscr, height_center, width_center, connection, work_duration, break_duration)


def _run_timer(
    stdscr: curses.window,
    height_center: int,
    width_center: int,
    connection: sqlite3.Connection,
    work_duration: int,
    break_duration: int
):
    session_id, start_time = sess.create_session(connection, work_duration, break_duration)
    stdscr.timeout(1000)

    try:
        while True:
            elapsed_time = int((datetime.now() - start_time).total_seconds())
            is_done = elapsed_time >= work_duration + break_duration

            if elapsed_time < work_duration:
                phase = "WORK"
                time_remaining = work_duration - elapsed_time
                bar_elapsed = elapsed_time
                bar_total = work_duration
            else:
                phase = "BREAK"
                time_remaining = work_duration + break_duration - elapsed_time
                bar_elapsed = elapsed_time - work_duration
                bar_total = break_duration

            hours = time_remaining // 3600
            minutes = (time_remaining - hours * 3600) // 60
            seconds = time_remaining - hours * 3600 - minutes * 60
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}"

            stdscr.clear()

            phase_attr = curses.A_BOLD
            phase_col = width_center - len(phase) // 2
            stdscr.addstr(height_center - 9, phase_col, phase, phase_attr)

            stdscr.addstr(height_center - 8, width_center - 12, "─" * 24)

            _render_big_time(stdscr, height_center - 7, width_center, time_str)

            stdscr.addstr(height_center - 1, width_center - 12, "─" * 24)

            _draw_progress_bar(stdscr, height_center, width_center, bar_elapsed, bar_total)

            pct = int((bar_elapsed / bar_total) * 100) if bar_total > 0 else 0
            pct_str = f"{pct}%"
            stdscr.addstr(height_center + 1, width_center - len(pct_str) // 2, pct_str)

            stdscr.addstr(height_center + 3, width_center - 12, "─" * 24)
            stdscr.addstr(height_center + 4, width_center - 12, "  q  stop session        ")

            stdscr.refresh()

            if is_done:
                sess.end_session(connection, session_id, start_time, work_duration)
                sess.notify("Pomodoro", "Session complete! Time for a break.")
                stdscr.clear()
                msg = "Session complete! Well done."
                stdscr.addstr(height_center, width_center - len(msg) // 2, msg, curses.A_BOLD)
                stdscr.addstr(height_center + 2, width_center - 12, "Press any key to continue")
                stdscr.refresh()
                stdscr.timeout(-1)
                stdscr.getch()
                break

            key = stdscr.getch()
            if key == ord("q"):
                sess.end_session(connection, session_id, start_time, work_duration)
                sess.notify("Pomodoro", "Session stopped early.")
                break
    finally:
        stdscr.timeout(-1)
