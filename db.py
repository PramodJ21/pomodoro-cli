from datetime import date, datetime, timedelta
import sqlite3
from pathlib import Path
import os



def get_db_path() -> Path:
    target_dir = os.environ.get("XDG_DATA_HOME")
    if not target_dir:
        target_dir = Path.home() / ".local/share/pomodoro_cli"
    else:
        target_dir = Path(target_dir) / "pomodoro_cli"

    target_dir.mkdir(parents=True, exist_ok=True)
    db_path = target_dir / "pomodoro_cli.db"
    return db_path


def get_connection() -> sqlite3.Connection:
    db_path = get_db_path()
    connection = sqlite3.connect(str(db_path))
    return connection



def initialize_db(connection: sqlite3.Connection) -> None:
    cursor = connection.cursor()

    # Creating Initial Tables
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS session(
        session_id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_time datetime NOT NULL,
        work_duration INTEGER NOT NULL,
        break_duration INTEGER NOT NULL,
        session_duration INTEGER DEFAULT NULL
            )""")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings(
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
            )""")
        connection.commit()
    except sqlite3.Error as e:
        connection.rollback()
        raise e

def get_setting(connection: sqlite3.Connection, key: str, default: str = "") -> str:
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row[0] if row else default
    except sqlite3.Error:
        return default

def set_setting(connection: sqlite3.Connection, key: str, value: str) -> None:
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(value)))
        connection.commit()
    except sqlite3.Error as e:
        connection.rollback()
        raise e

def create_session(connection: sqlite3.Connection,
    start_time: datetime,
    work_duration: int,
    break_duration: int
):
    cursor = connection.cursor()
    query = "INSERT INTO session (start_time, work_duration, break_duration) VALUES (?,?,?) RETURNING *"
    try:
        cursor.execute(query, (start_time, work_duration, break_duration))
        row = cursor.fetchone()
        connection.commit()
        return row
    except sqlite3.Error as e:
        connection.rollback()
        raise e

def update_session(
    connection: sqlite3.Connection,
    session_id: int,
    session_duration: int
):
    cursor = connection.cursor()
    query = "UPDATE session SET session_duration = ? WHERE session_id = ?"
    try:
        cursor.execute(query, (session_duration, session_id))
        connection.commit()
        return cursor.rowcount
    except sqlite3.Error as e:
        connection.rollback()
        raise e

def get_session_stats_daily(connection: sqlite3.Connection, days: int = 7):
    all_dates = [datetime.now().date() - timedelta(days=i) for i in range(days)]
    min_date = str(all_dates[-1])

    cursor = connection.cursor()
    query = """
    SELECT date(start_time), SUM(session_duration)
    FROM session
    WHERE date(start_time) >= ?
    GROUP BY date(start_time)
    ORDER BY date(start_time) DESC;
    """

    try:
        cursor.execute(query, (min_date,))
        session_stats = cursor.fetchall()
    except sqlite3.Error as e:
        connection.rollback()
        raise e

    stats_dict = {row[0]: (row[1] or 0) for row in session_stats}
    temp_stats = [(str(d), stats_dict.get(str(d), 0)) for d in all_dates]

    return temp_stats

def get_session_stats_weekly(connection: sqlite3.Connection):
    all_dates = [datetime.now().date() - timedelta(days=i) for i in range(28)]
    min_date = str(all_dates[-1])

    cursor = connection.cursor()
    query = """
    SELECT date(start_time), SUM(session_duration)
    FROM session
    WHERE date(start_time) >= ?
    GROUP BY date(start_time)
    ORDER BY date(start_time) DESC;
    """
    try:
        cursor.execute(query, (min_date,))
        session_stats = cursor.fetchall()
    except sqlite3.Error as e:
        connection.rollback()
        raise e

    stats_dict = {row[0]: (row[1] or 0) for row in session_stats}
    temp_stats = [(str(d), stats_dict.get(str(d), 0)) for d in all_dates]

    last_7_days = sum(s[1] for s in temp_stats[:7])
    last_14_days = sum(s[1] for s in temp_stats[:14])
    last_21_days = sum(s[1] for s in temp_stats[:21])
    last_28_days = sum(s[1] for s in temp_stats[:28])

    return last_7_days, last_14_days, last_21_days, last_28_days

def get_lifetime_stats(connection: sqlite3.Connection) -> dict:
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT COUNT(*), COALESCE(SUM(session_duration), 0), COALESCE(MAX(session_duration), 0)
            FROM session
            WHERE session_duration > 0
        """)
        total_count, total_seconds, max_seconds = cursor.fetchone()

        today_str = str(datetime.now().date())
        cursor.execute("""
            SELECT COUNT(*), COALESCE(SUM(session_duration), 0)
            FROM session
            WHERE date(start_time) = ? AND session_duration > 0
        """, (today_str,))
        today_count, today_seconds = cursor.fetchone()

        cursor.execute("""
            SELECT strftime('%w', start_time) as dow, COALESCE(SUM(session_duration), 0) as total
            FROM session
            WHERE session_duration > 0
            GROUP BY dow
            ORDER BY total DESC
            LIMIT 1
        """)
        best_dow_row = cursor.fetchone()
        dow_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        if best_dow_row and best_dow_row[1] > 0:
            best_day = (dow_names[int(best_dow_row[0])], best_dow_row[1])
        else:
            best_day = ("None yet", 0)

        avg_session = total_seconds // total_count if total_count > 0 else 0

        return {
            "total_count": total_count,
            "total_seconds": total_seconds,
            "max_seconds": max_seconds,
            "avg_seconds": avg_session,
            "today_count": today_count,
            "today_seconds": today_seconds,
            "best_day": best_day,
        }
    except sqlite3.Error as e:
        connection.rollback()
        raise e

def get_streaks(connection: sqlite3.Connection) -> tuple[int, int]:
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT DISTINCT date(start_time)
            FROM session
            WHERE session_duration > 0
            ORDER BY date(start_time) DESC
        """)
        rows = [datetime.strptime(r[0], "%Y-%m-%d").date() for r in cursor.fetchall()]
        if not rows:
            return 0, 0

        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        current_streak = 0
        expected = today if (rows and rows[0] == today) else yesterday
        if rows and (rows[0] == today or rows[0] == yesterday):
            for d in rows:
                if d == expected:
                    current_streak += 1
                    expected -= timedelta(days=1)
                elif d > expected:
                    continue
                else:
                    break

        dates_asc = sorted(rows)
        best_streak = 0
        streak = 0
        prev_d = None
        for d in dates_asc:
            if prev_d is None:
                streak = 1
            elif d == prev_d + timedelta(days=1):
                streak += 1
            elif d == prev_d:
                pass
            else:
                streak = 1
            prev_d = d
            if streak > best_streak:
                best_streak = streak

        return current_streak, best_streak
    except sqlite3.Error as e:
        connection.rollback()
        raise e

def get_heatmap_data(connection: sqlite3.Connection, weeks: int = 4):
    total_days = weeks * 7
    all_dates = [datetime.now().date() - timedelta(days=i) for i in range(total_days)]
    min_date = str(all_dates[-1])
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT date(start_time), SUM(session_duration)
            FROM session
            WHERE date(start_time) >= ?
            GROUP BY date(start_time)
        """, (min_date,))
        stats_dict = {r[0]: (r[1] or 0) for r in cursor.fetchall()}
        return [(d, stats_dict.get(str(d), 0)) for d in all_dates]
    except sqlite3.Error as e:
        connection.rollback()
        raise e
def truncate_db(connection: sqlite3.Connection):
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM session")
        connection.commit()
    except sqlite3.Error as e:
        connection.rollback()
        raise e
