import test from 'node:test';
import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';
import * as db from '../src/db.js';
import * as animations from '../src/interface/animations.js';
import * as utils from '../src/utils.js';

test('Database sync in-memory operations', () => {
  const memDb = new DatabaseSync(':memory:');
  db.initializeDb(memDb);

  // Settings test
  db.setSetting(memDb, 'theme', 'matrix');
  assert.equal(db.getSetting(memDb, 'theme'), 'matrix');
  assert.equal(db.getSetting(memDb, 'nonexistent', 'default_val'), 'default_val');

  // Session lifecycle test
  const startIso = '2026-11-02 10:00:00.000000';
  const rowId = db.createSession(memDb, startIso, 1500, 300);
  assert.ok(rowId > 0, 'rowId should be positive integer');

  db.updateSession(memDb, rowId, 1500);

  const daily = db.getSessionStatsDaily(memDb);
  assert.equal(daily.length, 7);

  const weekly = db.getSessionStatsWeekly(memDb);
  assert.equal(weekly.length, 4);

  const lifetime = db.getLifetimeStats(memDb);
  assert.equal(lifetime.total_count, 1);
  assert.equal(lifetime.total_seconds, 1500);

  const [currentStreak, longestStreak] = db.getStreaks(memDb);
  assert.ok(currentStreak >= 0);
  assert.ok(longestStreak >= 0);

  const heatmap = db.getHeatmapData(memDb);
  assert.equal(heatmap.length, 28);

  memDb.close();
});

test('All 14 animation themes render valid uniform frames', () => {
  assert.equal(animations.THEMES.length, 14);

  for (const theme of animations.THEMES) {
    for (const phase of ['WORK', 'BREAK', 'OVERTIME']) {
      for (let frame = 0; frame < 8; frame++) {
        const [lines, caption] = animations.getAnimationLines(theme, phase, frame, 0.5);
        assert.ok(Array.isArray(lines), `Theme ${theme} ${phase} lines must be an array`);
        assert.equal(typeof caption, 'string', `Theme ${theme} ${phase} caption must be a string`);
        if (lines.length > 0) {
          const expectedLen = lines[0].length;
          for (let i = 0; i < lines.length; i++) {
            assert.equal(
              lines[i].length,
              expectedLen,
              `Theme ${theme} ${phase} frame ${frame} line ${i} has length ${lines[i].length}, expected ${expectedLen}`
            );
          }
        }
      }
    }
  }
});

test('Format duration utilities', () => {
  assert.equal(utils.fmtDuration(0), '0m');
  assert.equal(utils.fmtDuration(59), '0m');
  assert.equal(utils.fmtDuration(60), '1m');
  assert.equal(utils.fmtDuration(125), '2m');
  assert.equal(utils.fmtDuration(3600), '1h 00m');
  assert.equal(utils.fmtDuration(3665), '1h 01m');
  assert.equal(utils.fmtDuration(7325), '2h 02m');

  assert.equal(utils.fmtDurationShort(60), '1m');
  assert.equal(utils.fmtDurationShort(3600), '1h');
  assert.equal(utils.fmtDurationShort(3665), '1h1m');

  assert.equal(utils.visibleLength('Hello'), 5);
  assert.equal(utils.visibleLength('\x1b[31mHello\x1b[0m'), 5);
  assert.equal(utils.visibleLength('\x1b[1m\x1b[32mTest 123\x1b[0m'), 8);
});
