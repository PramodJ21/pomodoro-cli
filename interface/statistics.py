import curses
import sqlite3
import db


def _fmt_duration(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    if h > 0:
        return f"{h}h {m:02}m"
    return f"{m}m"


def _draw_horizontal_bars(stdscr: curses.window, start_row: int, width_center: int, stats: list, scale_seconds: int, bar_max: int = 30):
    for i, (date_str, seconds) in enumerate(stats):
        filled = int((seconds / scale_seconds) * bar_max)
        filled = min(filled, bar_max)
        bar = "█" * filled + "░" * (bar_max - filled)
        day_label = date_str[5:]
        duration = _fmt_duration(seconds).rjust(7)
        line = f"  {day_label}  {bar}  {duration}"
        stdscr.addstr(start_row + i, width_center - (bar_max + 20) // 2, line)


def StatisticsScreen(
    stdscr: curses.window,
    height_center: int,
    width_center: int,
    connection: sqlite3.Connection
):
    daily_stats = db.get_session_stats_daily(connection)
    last_7, last_14, last_21, last_28 = db.get_session_stats_weekly(connection)

    title = r"""
   ___ _____  _  _____ ___
  / __|_   _|/_\|_   _/ __|
  \__ \ | | / _ \ | | \__ \
  |___/ |_|/_/ \_\|_| |___/
    """

    while True:
        stdscr.clear()

        split_title = title.splitlines()
        row = 1
        longest = max(len(l) for l in split_title)
        col = width_center - longest // 2
        for line in split_title:
            stdscr.addstr(row, col, line)
            row += 1

        row += 1
        stdscr.addstr(row, width_center - 20, "─" * 40)
        row += 1

        label = "LAST 7 DAYS"
        stdscr.addstr(row, width_center - len(label) // 2, label, curses.A_BOLD)
        row += 1

        daily_scale = max(max((s[1] for s in daily_stats), default=0), 8 * 3600)
        _draw_horizontal_bars(stdscr, row, width_center, daily_stats, scale_seconds=daily_scale)
        row += len(daily_stats) + 1

        stdscr.addstr(row, width_center - 20, "─" * 40)
        row += 1

        stdscr.addstr(row, width_center - 20, "ROLLING TOTALS", curses.A_BOLD)
        row += 1

        periods = [
            ("Last  7 days", last_7),
            ("Last 14 days", last_14),
            ("Last 21 days", last_21),
            ("Last 28 days", last_28),
        ]

        period_scales = [7, 14, 21, 28]
        for (label, seconds), n_days in zip(periods, period_scales):
            scale = max(n_days * daily_scale, 1)
            filled = int((seconds / scale) * 30)
            filled = min(filled, 30)
            bar = "█" * filled + "░" * (30 - filled)
            duration = _fmt_duration(seconds).rjust(7)
            line = f"  {label}  {bar}  {duration}"
            stdscr.addstr(row, width_center - (30 + 24) // 2, line)
            row += 1

        row += 1
        stdscr.addstr(row, width_center - 20, "─" * 40)
        row += 1
        hint = "q  back"
        stdscr.addstr(row, width_center - len(hint) // 2, hint)

        stdscr.refresh()
        key = stdscr.getch()
        if key == ord("q"):
            break
