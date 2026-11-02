import curses
from datetime import datetime
import sqlite3
import db
import session as sess
from interface.animations import (
    get_animation_lines,
    get_next_theme,
    get_theme_display_name,
)

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
    "+": ["     ", "  █  ", "█████", "  █  ", "     "],
    "-": ["     ", "     ", "█████", "     ", "     "],
}


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


def _render_big_time(stdscr: curses.window, row: int, width_center: int, time_str: str, attr: int = 0) -> None:
    chars = list(time_str)
    total_width = len(chars) * 6 - 1
    col_start = width_center - total_width // 2

    for line_idx in range(5):
        col = col_start
        for ch in chars:
            segment = _DIGITS.get(ch, ["     "] * 5)[line_idx]
            safe_addstr(stdscr, row + line_idx, col, segment, attr)
            col += 6


def _draw_progress_bar(stdscr: curses.window, row: int, width_center: int, elapsed: int, total: int, width: int = 36) -> None:
    max_y, max_x = stdscr.getmaxyx()
    bar_width = min(width, max(10, max_x - 14))
    filled = int((elapsed / total) * bar_width) if total > 0 else 0
    filled = max(0, min(filled, bar_width))
    bar = "█" * filled + "░" * (bar_width - filled)
    col = width_center - bar_width // 2
    safe_addstr(stdscr, row, col, bar)


def SessionScreen(
    stdscr: curses.window,
    height_center: int,
    width_center: int,
    connection: sqlite3.Connection,
) -> None:
    session_times = [(25 * 60, 5 * 60), (50 * 60, 10 * 60), (75 * 60, 15 * 60), (110 * 60, 20 * 60)]
    labels = [
        "  25 min / 5 min break  ",
        "  50 min / 10 min break  ",
        "  75 min / 15 min break  ",
        "  110 min / 20 min break  ",
        "  Back  ",
    ]
    selected = 0
    title = r"""
    ____  _____ ____ ____ ___ ___  _   _
   / ___|| ____/ ___/ ___|_ _/ _ \| \ | |
   \___ \|  _| \___ \___ \| | | | |  \| |
    ___) | |___ ___) |__) | | |_| | |\  |
   |____/|_____|____/____/___\___/|_| \_|
    """

    while True:
        max_y, max_x = stdscr.getmaxyx()
        h_center = max_y // 2
        w_center = max_x // 2

        stdscr.clear()
        split_title = [line for line in title.splitlines() if line.strip()]
        row = max(1, h_center - len(split_title) - 4)
        for line in split_title:
            col = w_center - len(line) // 2
            safe_addstr(stdscr, row, col, line)
            row += 1

        safe_addstr(stdscr, row + 1, w_center - 12, "─" * 24)

        menu_start_row = row + 2
        for i, label in enumerate(labels):
            r = menu_start_row + i
            c = w_center - len(label) // 2
            if selected == i:
                safe_addstr(stdscr, r, c, label, curses.A_REVERSE | curses.A_BOLD)
            else:
                safe_addstr(stdscr, r, c, label)

        hint_divider_row = menu_start_row + len(labels) + 1
        safe_addstr(stdscr, hint_divider_row, w_center - 12, "─" * 24)
        hint = "↑↓ navigate   enter select"
        safe_addstr(stdscr, hint_divider_row + 1, w_center - len(hint) // 2, hint)

        stdscr.refresh()
        key = stdscr.getch()

        if key in (curses.KEY_UP, ord("k"), ord("K")):
            selected = (selected - 1) % len(labels)
        elif key in (curses.KEY_DOWN, ord("j"), ord("J")):
            selected = (selected + 1) % len(labels)
        elif key in (ord("\n"), curses.KEY_ENTER, ord("\r")):
            if selected == len(labels) - 1:
                break
            else:
                work_duration, break_duration = session_times[selected]
                _run_timer(stdscr, connection, work_duration, break_duration)


def _run_timer(
    stdscr: curses.window,
    connection: sqlite3.Connection,
    work_duration: int,
    break_duration: int,
) -> None:
    current_theme = db.get_setting(connection, "theme", "bonfire")
    session_id, start_time = sess.create_session(connection, work_duration, break_duration)

    phase = "WORK"
    work_ended_time: datetime | None = None
    break_start_time: datetime | None = None
    tick_count = 0
    overtime_seconds = 0
    saved_session = False

    # 250ms timeout for smooth animations and responsive keyboard input
    stdscr.timeout(250)

    try:
        while True:
            tick_count += 1
            frame_idx = tick_count // 2  # Advances animation frame every ~500ms
            max_y, max_x = stdscr.getmaxyx()
            width_center = max_x // 2
            now = datetime.now()

            # --- State Transitions ---
            if phase == "WORK":
                elapsed = int((now - start_time).total_seconds())
                if elapsed >= work_duration:
                    phase = "OVERTIME"
                    work_ended_time = now
                    overtime_seconds = 0
                    sess.notify("Pomodoro", "Work session complete! Start break or keep going?")
                    try:
                        curses.beep()
                    except curses.error:
                        pass

            elif phase == "OVERTIME":
                if work_ended_time:
                    overtime_seconds = int((now - work_ended_time).total_seconds())

            elif phase == "BREAK":
                if break_start_time:
                    break_elapsed = int((now - break_start_time).total_seconds())
                    if break_elapsed >= break_duration:
                        sess.notify("Pomodoro", "Break complete! Well done.")
                        stdscr.clear()
                        msg = "Break complete! Well done."
                        safe_addstr(stdscr, max_y // 2 - 1, width_center - len(msg) // 2, msg, curses.A_BOLD)
                        hint = "Press any key to return to menu"
                        safe_addstr(stdscr, max_y // 2 + 1, width_center - len(hint) // 2, hint)
                        stdscr.refresh()
                        stdscr.timeout(-1)
                        stdscr.getch()
                        break

            # --- Calculate display metrics based on phase ---
            if phase == "WORK":
                elapsed = int((now - start_time).total_seconds())
                time_remaining = max(0, work_duration - elapsed)
                hours = time_remaining // 3600
                minutes = (time_remaining - hours * 3600) // 60
                seconds = time_remaining - hours * 3600 - minutes * 60
                if hours > 0:
                    time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
                else:
                    time_str = f"{minutes:02}:{seconds:02}"
                bar_elapsed = min(elapsed, work_duration)
                bar_total = work_duration
                progress_pct = elapsed / work_duration if work_duration > 0 else 1.0
                pct = int(progress_pct * 100)
                phase_title = "── WORK ──"

            elif phase == "OVERTIME":
                hours = overtime_seconds // 3600
                minutes = (overtime_seconds - hours * 3600) // 60
                seconds = overtime_seconds - hours * 3600 - minutes * 60
                if hours > 0:
                    time_str = f"+{hours:02}:{minutes:02}:{seconds:02}"
                else:
                    time_str = f"+{minutes:02}:{seconds:02}"
                bar_elapsed = work_duration
                bar_total = work_duration
                progress_pct = 1.0
                pct = 100
                phase_title = "── OVERTIME (+EXTRA TIME) ──"

            else:  # BREAK
                break_elapsed = int((now - break_start_time).total_seconds()) if break_start_time else 0
                time_remaining = max(0, break_duration - break_elapsed)
                hours = time_remaining // 3600
                minutes = (time_remaining - hours * 3600) // 60
                seconds = time_remaining - hours * 3600 - minutes * 60
                if hours > 0:
                    time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
                else:
                    time_str = f"{minutes:02}:{seconds:02}"
                bar_elapsed = min(break_elapsed, break_duration)
                bar_total = break_duration
                progress_pct = break_elapsed / break_duration if break_duration > 0 else 1.0
                pct = int(progress_pct * 100)
                phase_title = "── BREAK ──"

            # --- Fetch Animation Frame ---
            anim_lines, anim_caption = get_animation_lines(current_theme, phase, frame_idx, progress_pct)

            stdscr.clear()

            # --- Layout Dimensions & Responsive Sizing ---
            total_content_height = len(anim_lines) + 1 + 1 + 5 + 1 + 2 + 1 + 3 if anim_lines else 16
            show_anim = bool(anim_lines and max_y >= 23)

            if show_anim:
                total_height = len(anim_lines) + (1 if anim_caption else 0) + 14
            else:
                total_height = 14

            start_row = max(1, (max_y - total_height) // 2)
            row = start_row

            # Phase header
            safe_addstr(stdscr, row, width_center - len(phase_title) // 2, phase_title, curses.A_BOLD)
            row += 1

            # Animation & Caption
            if show_anim:
                for a_line in anim_lines:
                    safe_addstr(stdscr, row, width_center - len(a_line) // 2, a_line)
                    row += 1
                if anim_caption:
                    safe_addstr(stdscr, row, width_center - len(anim_caption) // 2, anim_caption, curses.A_DIM)
                    row += 1
            elif anim_caption and max_y >= 18:
                safe_addstr(stdscr, row, width_center - len(anim_caption) // 2, anim_caption, curses.A_DIM)
                row += 1

            safe_addstr(stdscr, row, width_center - 15, "─" * 30)
            row += 1

            # Big Digital Clock
            _render_big_time(stdscr, row, width_center, time_str)
            row += 5

            safe_addstr(stdscr, row, width_center - 15, "─" * 30)
            row += 1

            # Progress Bar & Info
            _draw_progress_bar(stdscr, row, width_center, bar_elapsed, bar_total)
            row += 1

            if phase == "OVERTIME":
                extra_mins = overtime_seconds // 60
                extra_secs = overtime_seconds % 60
                status_text = f"Work Complete! +{extra_mins}m {extra_secs}s extra counted"
            else:
                status_text = f"{pct}%"
            safe_addstr(stdscr, row, width_center - len(status_text) // 2, status_text)
            row += 1

            safe_addstr(stdscr, row, width_center - 15, "─" * 30)
            row += 1

            # Hints & Controls
            theme_name = get_theme_display_name(current_theme)
            if phase == "WORK":
                hints = f"q stop   b take break   t theme ({theme_name})"
                safe_addstr(stdscr, row, width_center - len(hints) // 2, hints)
            elif phase == "OVERTIME":
                prompt = "enter / b Start Break   |   q Save & Exit"
                safe_addstr(stdscr, row, width_center - len(prompt) // 2, prompt, curses.A_BOLD)
                row += 1
                theme_hint = f"t theme ({theme_name})"
                safe_addstr(stdscr, row, width_center - len(theme_hint) // 2, theme_hint)
            else:  # BREAK
                hints = f"q finish break   t theme ({theme_name})"
                safe_addstr(stdscr, row, width_center - len(hints) // 2, hints)

            stdscr.refresh()

            # --- User Input Handling ---
            key = stdscr.getch()

            # Cycle theme with 't', 'T', or Tab (ASCII 9)
            if key in (ord("t"), ord("T"), 9):
                current_theme = get_next_theme(current_theme)
                db.set_setting(connection, "theme", current_theme)

            elif phase == "WORK":
                if key in (ord("q"), ord("Q")):
                    elapsed = int((now - start_time).total_seconds())
                    sess.end_session(connection, session_id, elapsed)
                    saved_session = True
                    sess.notify("Pomodoro", "Session stopped early.")
                    break
                elif key in (ord("b"), ord("B")):
                    elapsed = int((now - start_time).total_seconds())
                    sess.end_session(connection, session_id, elapsed)
                    saved_session = True
                    phase = "BREAK"
                    break_start_time = now
                    sess.notify("Pomodoro", "Break started early.")

            elif phase == "OVERTIME":
                if key in (ord("q"), ord("Q")):
                    total_work = work_duration + overtime_seconds
                    sess.end_session(connection, session_id, total_work)
                    saved_session = True
                    sess.notify("Pomodoro", f"Session saved: {total_work // 60}m focused!")
                    break
                elif key in (ord("\n"), curses.KEY_ENTER, ord("\r"), ord("b"), ord("B"), ord(" ")):
                    total_work = work_duration + overtime_seconds
                    sess.end_session(connection, session_id, total_work)
                    saved_session = True
                    phase = "BREAK"
                    break_start_time = now
                    sess.notify("Pomodoro", "Break started. Take some rest!")

            elif phase == "BREAK":
                if key in (ord("q"), ord("Q"), 27):
                    break

    finally:
        stdscr.timeout(-1)
        if not saved_session:
            now = datetime.now()
            if phase == "WORK":
                elapsed = int((now - start_time).total_seconds())
                sess.end_session(connection, session_id, elapsed)
            elif phase in ("OVERTIME", "BREAK"):
                total_work = work_duration + overtime_seconds
                sess.end_session(connection, session_id, total_work)
