import path from 'node:path';
import os from 'node:os';
import fs from 'node:fs';
import { DatabaseSync } from 'node:sqlite';

export function getDbPath() {
  const targetDir = process.env.XDG_DATA_HOME
    ? path.join(process.env.XDG_DATA_HOME, 'pomodoro_cli')
    : path.join(os.homedir(), '.local', 'share', 'pomodoro_cli');

  fs.mkdirSync(targetDir, { recursive: true });
  return path.join(targetDir, 'pomodoro_cli.db');
}

export function getConnection() {
  const dbPath = getDbPath();
  const db = new DatabaseSync(dbPath);
  return db;
}

export function initializeDb(db) {
  db.exec(`
    CREATE TABLE IF NOT EXISTS session (
      session_id INTEGER PRIMARY KEY AUTOINCREMENT,
      start_time datetime NOT NULL,
      work_duration INTEGER NOT NULL,
      break_duration INTEGER NOT NULL,
      session_duration INTEGER DEFAULT NULL
    );
    CREATE TABLE IF NOT EXISTS settings (
      key TEXT PRIMARY KEY,
      value TEXT NOT NULL
    );
  `);
}

export function getSetting(db, key, defaultValue = '') {
  try {
    const row = db.prepare('SELECT value FROM settings WHERE key = ?').get(key);
    return row ? row.value : defaultValue;
  } catch {
    return defaultValue;
  }
}

export function setSetting(db, key, value) {
  db.prepare('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)').run(key, String(value));
}

export function createSession(db, startTime, workDuration, breakDuration) {
  // Format Date to ISO string compatible with Python datetime (YYYY-MM-DD HH:MM:SS)
  const timeStr = typeof startTime === 'string'
    ? startTime
    : startTime.toISOString().replace('T', ' ').slice(0, 19);

  const info = db.prepare(`
    INSERT INTO session (start_time, work_duration, break_duration)
    VALUES (?, ?, ?)
  `).run(timeStr, workDuration, breakDuration);

  return Number(info.lastInsertRowid);
}

export function updateSession(db, sessionId, sessionDuration) {
  const info = db.prepare(`
    UPDATE session SET session_duration = ? WHERE session_id = ?
  `).run(sessionDuration, sessionId);

  return info.changes;
}

export function getSessionStatsDaily(db, days = 7) {
  const allDates = Array.from({ length: days }, (_, i) => {
    const d = new Date();
    d.setDate(d.getDate() - i);
    return d.toISOString().slice(0, 10);
  });
  const minDate = allDates[allDates.length - 1];

  const rows = db.prepare(`
    SELECT date(start_time) as dt, SUM(session_duration) as total
    FROM session
    WHERE date(start_time) >= ?
    GROUP BY dt
    ORDER BY dt DESC
  `).all(minDate);

  const statsMap = new Map(rows.map((r) => [r.dt, Number(r.total || 0)]));
  return allDates.map((d) => [d, statsMap.get(d) || 0]);
}

export function getSessionStatsWeekly(db) {
  const allDates = Array.from({ length: 28 }, (_, i) => {
    const d = new Date();
    d.setDate(d.getDate() - i);
    return d.toISOString().slice(0, 10);
  });
  const minDate = allDates[allDates.length - 1];

  const rows = db.prepare(`
    SELECT date(start_time) as dt, SUM(session_duration) as total
    FROM session
    WHERE date(start_time) >= ?
    GROUP BY dt
    ORDER BY dt DESC
  `).all(minDate);

  const statsMap = new Map(rows.map((r) => [r.dt, Number(r.total || 0)]));
  const daily = allDates.map((d) => [d, statsMap.get(d) || 0]);

  const last7 = daily.slice(0, 7).reduce((acc, s) => acc + s[1], 0);
  const last14 = daily.slice(0, 14).reduce((acc, s) => acc + s[1], 0);
  const last21 = daily.slice(0, 21).reduce((acc, s) => acc + s[1], 0);
  const last28 = daily.slice(0, 28).reduce((acc, s) => acc + s[1], 0);

  return [last7, last14, last21, last28];
}

export function getLifetimeStats(db) {
  const lifetime = db.prepare(`
    SELECT
      COUNT(*) as count,
      COALESCE(SUM(session_duration), 0) as total,
      COALESCE(MAX(session_duration), 0) as max_dur
    FROM session
    WHERE session_duration > 0
  `).get() || { count: 0, total: 0, max_dur: 0 };

  const todayStr = new Date().toISOString().slice(0, 10);
  const todayRow = db.prepare(`
    SELECT
      COUNT(*) as count,
      COALESCE(SUM(session_duration), 0) as total
    FROM session
    WHERE date(start_time) = ? AND session_duration > 0
  `).get(todayStr) || { count: 0, total: 0 };

  const bestDowRow = db.prepare(`
    SELECT strftime('%w', start_time) as dow, COALESCE(SUM(session_duration), 0) as total
    FROM session
    WHERE session_duration > 0
    GROUP BY dow
    ORDER BY total DESC
    LIMIT 1
  `).get();

  const dowNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  let bestDay = ['None yet', 0];
  if (bestDowRow && Number(bestDowRow.total) > 0) {
    bestDay = [dowNames[Number(bestDowRow.dow)], Number(bestDowRow.total)];
  }

  const totalCount = Number(lifetime.count);
  const totalSeconds = Number(lifetime.total);
  const maxSeconds = Number(lifetime.max_dur);
  const avgSeconds = totalCount > 0 ? Math.floor(totalSeconds / totalCount) : 0;

  return {
    total_count: totalCount,
    total_seconds: totalSeconds,
    max_seconds: maxSeconds,
    avg_seconds: avgSeconds,
    today_count: Number(todayRow.count),
    today_seconds: Number(todayRow.total),
    best_day: bestDay,
  };
}

export function getStreaks(db) {
  const rows = db.prepare(`
    SELECT DISTINCT date(start_time) as dt
    FROM session
    WHERE session_duration > 0
    ORDER BY dt DESC
  `).all().map((r) => r.dt);

  if (rows.length === 0) return [0, 0];

  const todayStr = new Date().toISOString().slice(0, 10);
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  const yesterdayStr = yesterday.toISOString().slice(0, 10);

  // Current streak
  let currentStreak = 0;
  if (rows[0] === todayStr || rows[0] === yesterdayStr) {
    let expected = new Date(rows[0] + 'T00:00:00');
    for (const dStr of rows) {
      const cur = new Date(dStr + 'T00:00:00');
      const diffDays = Math.round((expected.getTime() - cur.getTime()) / (1000 * 60 * 60 * 24));
      if (diffDays === 0) {
        currentStreak++;
        expected.setDate(expected.getDate() - 1);
      } else if (diffDays < 0) {
        continue;
      } else {
        break;
      }
    }
  }

  // Best streak
  const sortedDates = [...rows].sort();
  let bestStreak = 0;
  let streak = 0;
  let prev = null;

  for (const dStr of sortedDates) {
    const cur = new Date(dStr + 'T00:00:00');
    if (!prev) {
      streak = 1;
    } else {
      const diffDays = Math.round((cur.getTime() - prev.getTime()) / (1000 * 60 * 60 * 24));
      if (diffDays === 1) {
        streak++;
      } else if (diffDays === 0) {
        // same date
      } else {
        streak = 1;
      }
    }
    prev = cur;
    if (streak > bestStreak) bestStreak = streak;
  }

  return [currentStreak, bestStreak];
}

export function getHeatmapData(db, weeks = 4) {
  const totalDays = weeks * 7;
  const allDates = Array.from({ length: totalDays }, (_, i) => {
    const d = new Date();
    d.setDate(d.getDate() - i);
    return d.toISOString().slice(0, 10);
  });
  const minDate = allDates[allDates.length - 1];

  const rows = db.prepare(`
    SELECT date(start_time) as dt, SUM(session_duration) as total
    FROM session
    WHERE date(start_time) >= ?
    GROUP BY dt
  `).all(minDate);

  const statsMap = new Map(rows.map((r) => [r.dt, Number(r.total || 0)]));
  return allDates.map((d) => [d, statsMap.get(d) || 0]);
}
