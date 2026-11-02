import curses
from datetime import datetime, timedelta
import sqlite3
import db


def _fmt_duration(seconds: int) -> str:
    """Formats seconds into human readable duration."""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    if h > 0:
        return f"{h}h {m:02}m"
    return f"{m}m"


def _fmt_duration_short(seconds: int) -> str:
    """Short format for tight spaces like chart axes."""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    if h > 0 and m > 0:
        return f"{h}h{m}m"
    elif h > 0:
        return f"{h}h"
    return f"{m}m"


def safe_addstr(stdscr: curses.window, row: int, col: int, text: str, attr: int = 0) -> None:
    """Safely writes a string within terminal boundaries without throwing curses errors."""
    max_y, max_x = stdscr.getmaxyx()
    if row < 0 or row >= max_y or col >= max_x:
        return
    if col < 0:
        text = text[-col:]
        col = 0
    if col + len(text) >= max_x:
        text = text[: max_x - col - 1]
    if not text:
        return
    try:
        if attr:
            stdscr.addstr(row, col, text, attr)
        else:
            stdscr.addstr(row, col, text)
    except curses.error:
        pass


def _draw_horizontal_bars(stdscr: curses.window, start_row: int, width_center: int, stats: list, scale_seconds: int, bar_max: int = 28) -> None:
    dow_abbrs = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, (date_str, seconds) in enumerate(stats):
        d_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        dow = dow_abbrs[d_obj.weekday()]
        filled = int((seconds / scale_seconds) * bar_max) if scale_seconds > 0 else 0
        filled = max(0, min(filled, bar_max))
        bar = "█" * filled + "░" * (bar_max - filled)
        day_label = f"{date_str[5:]} ({dow})"
        duration = _fmt_duration(seconds).rjust(7)
        line = f"  {day_label}  {bar}  {duration}"
        safe_addstr(stdscr, start_row + i, width_center - (bar_max + 24) // 2, line)


def _render_bars_view(stdscr: curses.window, row: int, width_center: int, daily_stats: list, rolling_stats: tuple) -> int:
    """View 0: Horizontal bar chart & rolling multi-week totals."""
    safe_addstr(stdscr, row, width_center - 12, "LAST 7 DAYS (BARS)", curses.A_BOLD)
    row += 1

    daily_scale = max(max((s[1] for s in daily_stats), default=0), 8 * 3600)
    _draw_horizontal_bars(stdscr, row, width_center, daily_stats, scale_seconds=daily_scale)
    row += len(daily_stats)

    safe_addstr(stdscr, row, width_center - 22, "─" * 44)
    row += 1

    safe_addstr(stdscr, row, width_center - 20, "ROLLING TOTALS", curses.A_BOLD)
    row += 1

    last_7, last_14, last_21, last_28 = rolling_stats
    periods = [
        ("Last  7 days", last_7),
        ("Last 14 days", last_14),
        ("Last 21 days", last_21),
        ("Last 28 days", last_28),
    ]

    period_scales = [7, 14, 21, 28]
    for (label, seconds), n_days in zip(periods, period_scales):
        scale = max(n_days * daily_scale, 1)
        filled = int((seconds / scale) * 28)
        filled = max(0, min(filled, 28))
        bar = "█" * filled + "░" * (28 - filled)
        duration = _fmt_duration(seconds).rjust(7)
        line = f"  {label}  {bar}  {duration}"
        safe_addstr(stdscr, row, width_center - (28 + 24) // 2, line)
        row += 1

    return row


def _render_histogram_view(stdscr: curses.window, row: int, width_center: int, daily_stats: list) -> int:
    """View 1: Vertical column histogram for the last 7 days."""
    safe_addstr(stdscr, row, width_center - 14, "WEEKLY COLUMN HISTOGRAM", curses.A_BOLD)
    row += 1

    # Chronological: oldest (6 days ago) to newest (today)
    chrono_stats = list(reversed(daily_stats))
    max_sec = max(max((s[1] for s in chrono_stats), default=0), 3600)
    chart_height = 6

    dow_abbrs = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    col_width = 5  # Each day is 5 chars wide
    chart_content_width = 7 * col_width + 8
    chart_start_col = width_center - chart_content_width // 2

    for lvl in range(chart_height - 1, -1, -1):
        thresh_full = (lvl + 0.65) / chart_height
        thresh_half = (lvl + 0.20) / chart_height

        # Y-axis label
        if lvl == chart_height - 1:
            y_label = _fmt_duration_short(max_sec).rjust(5)
        elif lvl == chart_height // 2:
            y_label = _fmt_duration_short(max_sec // 2).rjust(5)
        elif lvl == 0:
            y_label = "   0m"
        else:
            y_label = "     "

        bar_line = f"{y_label} │ "
        for _, sec in chrono_stats:
            frac = sec / max_sec if max_sec > 0 else 0
            if frac >= thresh_full:
                segment = " ███ "
            elif frac >= thresh_half:
                segment = " ▄▄▄ "
            else:
                segment = "     "
            bar_line += segment

        safe_addstr(stdscr, row, chart_start_col, bar_line)
        row += 1

    # Baseline axis
    axis_line = "      └" + "─────" * 7
    safe_addstr(stdscr, row, chart_start_col, axis_line)
    row += 1

    # Day of week labels
    dow_line = "        "
    for date_str, _ in chrono_stats:
        d_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        dow = dow_abbrs[d_obj.weekday()]
        dow_line += f" {dow}  "
    safe_addstr(stdscr, row, chart_start_col, dow_line)
    row += 1

    # Date labels (MM/DD)
    date_line = "        "
    for date_str, _ in chrono_stats:
        mmdd = date_str[5:].replace("-", "/")
        date_line += f"{mmdd} "
    safe_addstr(stdscr, row, chart_start_col, date_line, curses.A_DIM)
    row += 1

    # Duration labels
    dur_line = "        "
    for _, sec in chrono_stats:
        d_str = _fmt_duration_short(sec).center(5)
        dur_line += d_str
    safe_addstr(stdscr, row, chart_start_col, dur_line, curses.A_BOLD)
    row += 1

    safe_addstr(stdscr, row, width_center - 22, "─" * 44)
    row += 1

    # Summary
    total_7d = sum(s[1] for s in chrono_stats)
    daily_avg = total_7d // 7
    summary = f"7-Day Total: {_fmt_duration(total_7d)}  •  Daily Avg: {_fmt_duration(daily_avg)}"
    safe_addstr(stdscr, row, width_center - len(summary) // 2, summary)
    row += 1

    return row


def _render_heatmap_view(stdscr: curses.window, row: int, width_center: int, connection: sqlite3.Connection) -> int:
    """View 2: 4-week calendar contribution heatmap & streaks."""
    safe_addstr(stdscr, row, width_center - 15, "4-WEEK FOCUS HEATMAP & STREAKS", curses.A_BOLD)
    row += 1

    heatmap_data = db.get_heatmap_data(connection, weeks=4)
    cur_streak, best_streak = db.get_streaks(connection)
    stats_dict = {d: sec for d, sec in heatmap_data}

    today = datetime.now().date()
    start_of_this_week = today - timedelta(days=today.weekday())
    start_date = start_of_this_week - timedelta(weeks=3)

    dow_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    table_start_col = width_center - 16

    header = "       Wk-3  Wk-2  Wk-1  This"
    safe_addstr(stdscr, row, table_start_col, header, curses.A_DIM)
    row += 1

    for d_idx in range(7):
        line = f"  {dow_labels[d_idx]}  "
        for w_idx in range(4):
            cur_date = start_date + timedelta(weeks=w_idx, days=d_idx)
            if cur_date > today:
                cell = " ·  "
            else:
                sec = stats_dict.get(cur_date, 0)
                if sec == 0:
                    cell = " ░  "
                elif sec < 1800:
                    cell = " ▒  "
                elif sec < 3600:
                    cell = " ▓  "
                else:
                    cell = " █  "
            line += cell
        safe_addstr(stdscr, row, table_start_col, line)
        row += 1

    safe_addstr(stdscr, row, width_center - 22, "─" * 44)
    row += 1

    legend = "Legend: ░ 0m   ▒ <30m   ▓ 30-60m   █ 1h+"
    safe_addstr(stdscr, row, width_center - len(legend) // 2, legend, curses.A_DIM)
    row += 1

    # 28-day stats
    total_28d = sum(sec for _, sec in heatmap_data)
    active_days = sum(1 for _, sec in heatmap_data if sec > 0)
    month_summary = f"Past 28 Days: {_fmt_duration(total_28d)}  •  Active: {active_days}/28 days"
    safe_addstr(stdscr, row, width_center - len(month_summary) // 2, month_summary)
    row += 1

    streaks_text = f"🔥 Current Streak: {cur_streak} days   ★ Best Streak: {best_streak} days"
    safe_addstr(stdscr, row, width_center - len(streaks_text) // 2, streaks_text, curses.A_BOLD)
    row += 1

    return row


def _render_records_view(stdscr: curses.window, row: int, width_center: int, connection: sqlite3.Connection) -> int:
    """View 3: Lifetime records, milestones, and rank."""
    safe_addstr(stdscr, row, width_center - 13, "LIFETIME RECORDS & RANK", curses.A_BOLD)
    row += 1

    stats = db.get_lifetime_stats(connection)
    cur_streak, best_streak = db.get_streaks(connection)

    total_sec = stats["total_seconds"]
    if total_sec < 5 * 3600:
        rank_title = "Apprentice Novice ✦"
    elif total_sec < 20 * 3600:
        rank_title = "Journeyman Adept ⚔"
    elif total_sec < 50 * 3600:
        rank_title = "Master of Focus 🛡"
    else:
        rank_title = "Grandmaster Archmage 👑"

    card_width = 46
    card_start_col = width_center - card_width // 2

    safe_addstr(stdscr, row, card_start_col, f"┌{'─' * (card_width - 2)}┐")
    row += 1

    rank_line = f"  Rank: {rank_title}"
    safe_addstr(stdscr, row, card_start_col, f"│{rank_line.ljust(card_width - 2)}│", curses.A_BOLD)
    row += 1

    safe_addstr(stdscr, row, card_start_col, f"├{'─' * (card_width - 2)}┤")
    row += 1

    items = [
        f"  ⏱  Total Focus Time:       {_fmt_duration(stats['total_seconds'])}",
        f"  🎯 Completed Sessions:     {stats['total_count']} sessions",
        f"  🏆 Longest Session:        {_fmt_duration(stats['max_seconds'])}",
        f"  ⏳ Average Session:        {_fmt_duration(stats['avg_seconds'])}",
        f"  📅 Today's Focus:          {_fmt_duration(stats['today_seconds'])} ({stats['today_count']} sessions)",
        f"  🌟 Top Day of Week:        {stats['best_day'][0]} ({_fmt_duration(stats['best_day'][1])})",
        f"  🔥 Current Daily Streak:   {cur_streak} days",
        f"  ★  All-Time Best Streak:   {best_streak} days",
    ]

    for item in items:
        safe_addstr(stdscr, row, card_start_col, f"│{item.ljust(card_width - 2)}│")
        row += 1

    safe_addstr(stdscr, row, card_start_col, f"└{'─' * (card_width - 2)}┘")
    row += 1

    return row


def StatisticsScreen(
    stdscr: curses.window,
    height_center: int,
    width_center: int,
    connection: sqlite3.Connection,
) -> None:
    views = ["bars", "histogram", "heatmap", "records"]
    tab_names = ["1: Bars", "2: Columns", "3: Heatmap", "4: Records"]

    saved_view_str = db.get_setting(connection, "stats_view", "0")
    try:
        active_view = int(saved_view_str) % len(views)
    except ValueError:
        active_view = 0

    title_lines = [
        r" ___ _____  _  _____ ___ ",
        r"/ __|_   _|/_\|_   _/ __|",
        r"\__ \ | | / _ \ | | \__ \\",
        r"|___/ |_|/_/ \_\|_| |___/",
    ]

    while True:
        max_y, max_x = stdscr.getmaxyx()
        width_center = max_x // 2
        stdscr.clear()

        if max_y < 18 or max_x < 46:
            msg = "Window too small for statistics"
            hint = "Resize window or press 'q' to go back"
            safe_addstr(stdscr, max_y // 2 - 1, width_center - len(msg) // 2, msg, curses.A_BOLD)
            safe_addstr(stdscr, max_y // 2 + 1, width_center - len(hint) // 2, hint)
            stdscr.refresh()
            key = stdscr.getch()
            if key in (ord("q"), ord("Q"), 27):
                break
            continue

        # Fetch data
        daily_stats = db.get_session_stats_daily(connection)
        rolling_stats = db.get_session_stats_weekly(connection)

        total_content_rows = 22
        start_row = max(1, (max_y - total_content_rows) // 2) if max_y >= 23 else 0
        row = start_row

        # Title
        for line in title_lines:
            safe_addstr(stdscr, row, width_center - len(line) // 2, line)
            row += 1

        # Interactive Tab Bar
        tab_bar_col = width_center - 22
        tab_str = ""
        current_col = tab_bar_col
        for idx, t_name in enumerate(tab_names):
            label = f" {t_name} "
            if idx == active_view:
                safe_addstr(stdscr, row, current_col, label, curses.A_REVERSE | curses.A_BOLD)
            else:
                safe_addstr(stdscr, row, current_col, label, curses.A_DIM)
            current_col += len(label) + 2
        row += 1

        safe_addstr(stdscr, row, width_center - 22, "─" * 44)
        row += 1

        # Active View Rendering
        if active_view == 0:
            row = _render_bars_view(stdscr, row, width_center, daily_stats, rolling_stats)
        elif active_view == 1:
            row = _render_histogram_view(stdscr, row, width_center, daily_stats)
        elif active_view == 2:
            row = _render_heatmap_view(stdscr, row, width_center, connection)
        elif active_view == 3:
            row = _render_records_view(stdscr, row, width_center, connection)

        # Footer Navigation Hints
        safe_addstr(stdscr, row, width_center - 22, "─" * 44)
        row += 1
        hint = "←/→ / Tab switch view   1-4 jump   q back"
        safe_addstr(stdscr, row, width_center - len(hint) // 2, hint)

        stdscr.refresh()
        key = stdscr.getch()

        if key in (ord("q"), ord("Q"), 27):
            break
        elif key in (curses.KEY_RIGHT, ord("l"), ord("L"), 9):  # 9 is Tab
            active_view = (active_view + 1) % len(views)
            db.set_setting(connection, "stats_view", str(active_view))
        elif key in (curses.KEY_LEFT, ord("h"), ord("H"), curses.KEY_BTAB):
            active_view = (active_view - 1) % len(views)
            db.set_setting(connection, "stats_view", str(active_view))
        elif key == ord("1"):
            active_view = 0
            db.set_setting(connection, "stats_view", str(active_view))
        elif key == ord("2"):
            active_view = 1
            db.set_setting(connection, "stats_view", str(active_view))
        elif key == ord("3"):
            active_view = 2
            db.set_setting(connection, "stats_view", str(active_view))
        elif key == ord("4"):
            active_view = 3
            db.set_setting(connection, "stats_view", str(active_view))
