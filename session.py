from datetime import datetime
import sqlite3
import subprocess
import db


def create_session(connection: sqlite3.Connection, work_duration: int, break_duration: int) -> tuple[int, datetime]:
    start_time = datetime.now()
    row = db.create_session(connection=connection, start_time=start_time, work_duration=work_duration, break_duration=break_duration)
    session_id = row[0]
    return session_id, start_time



def end_session(
    connection: sqlite3.Connection,
    session_id: int,
    duration_or_start_time: int | datetime,
    work_duration: int | None = None,
) -> None:
    if isinstance(duration_or_start_time, (int, float)):
        session_duration = int(duration_or_start_time)
    else:
        elapsed = int((datetime.now() - duration_or_start_time).total_seconds())
        session_duration = elapsed if work_duration is None else max(elapsed, work_duration)
    db.update_session(connection=connection, session_id=session_id, session_duration=session_duration)


def notify(title: str, message: str) -> None:
    subprocess.run(["notify-send", title, message], check=False)
