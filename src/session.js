import { spawn } from 'node:child_process';
import * as db from './db.js';

export function createSession(connection, workDuration, breakDuration) {
  const startTime = new Date();
  const sessionId = db.createSession(connection, startTime, workDuration, breakDuration);
  return { sessionId, startTime };
}

export function endSession(connection, sessionId, durationOrStartTime, workDuration = null) {
  let sessionDuration;
  if (typeof durationOrStartTime === 'number') {
    sessionDuration = Math.round(durationOrStartTime);
  } else if (durationOrStartTime instanceof Date) {
    const elapsed = Math.round((Date.now() - durationOrStartTime.getTime()) / 1000);
    sessionDuration = workDuration !== null ? Math.max(elapsed, workDuration) : elapsed;
  } else {
    sessionDuration = Math.round(Number(durationOrStartTime));
  }

  db.updateSession(connection, sessionId, sessionDuration);
}

export function notify(title, message) {
  try {
    const child = spawn('notify-send', [title, message], {
      stdio: 'ignore',
      detached: true,
    });
    child.unref();
  } catch {
    // Non-fatal if notify-send is not installed or available
  }
}
