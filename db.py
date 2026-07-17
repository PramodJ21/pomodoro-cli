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

    # Creating Inital Tables
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS session(
        session_id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_time datetime NOT NULL,
        work_duration INTEGER NOT NULL,
        break_duration INTEGER NOT NULL,
        session_duration INTEGER DEFAULT NULL
            )""")
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

def get_session_stats_daily(connection:sqlite3.Connection):
    cursor = connection.cursor()
    query = """
    SELECT date(start_time), SUM(session_duration)
    FROM session
    WHERE date(start_time) >= date('now', '-6 days')
    GROUP BY date(start_time)
    ORDER BY date(start_time) DESC;
    """

    try:
        cursor.execute(query)
        session_stats = cursor.fetchall()
    except sqlite3.Error as e:
        connection.rollback()
        raise e

    all_dates = [datetime.now().date() - timedelta(days=i) for i in range(7)]
    stats_dict = {row[0]: (row[1] or 0) for row in session_stats}
    temp_stats = [(str(d), stats_dict.get(str(d),0)) for d in  all_dates]

    return temp_stats

def get_session_stats_weekly(connection: sqlite3.Connection):
    cursor = connection.cursor()
    query = """
    SELECT date(start_time), SUM(session_duration)
    FROM session
    WHERE date(start_time) >= date('now', '-28 days')
    GROUP BY date(start_time)
    ORDER BY date(start_time) DESC;
    """
    try:
        cursor.execute(query)
        session_stats = cursor.fetchall()
    except sqlite3.Error as e:
        connection.rollback()
        raise e

    all_dates = [datetime.now().date() - timedelta(days=i) for i in range(28)]
    stats_dict = {row[0]: (row[1] or 0) for row in session_stats}
    temp_stats = [(str(d), stats_dict.get(str(d),0)) for d in  all_dates]

    last_7_days = sum(s[1] for s in temp_stats[:7])
    last_14_days = sum(s[1] for s in temp_stats[:14])
    last_21_days = sum(s[1] for s in temp_stats[:21])
    last_28_days = sum(s[1] for s in temp_stats[:28])

    return last_7_days, last_14_days, last_21_days, last_28_days
def truncate_db(connection: sqlite3.Connection):
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM session")
        connection.commit()
    except sqlite3.Error as e:
        connection.rollback()
        raise e
