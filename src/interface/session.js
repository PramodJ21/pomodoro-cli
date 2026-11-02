import * as db from '../db.js';
import * as sess from '../session.js';
import { style, visibleLength, beep } from '../utils.js';
import { getAnimationLines, getNextTheme, getThemeDisplayName } from './animations.js';

// ASCII digit segments — each digit is 5 lines tall
const DIGITS = {
  0: ['█████', '█   █', '█   █', '█   █', '█████'],
  1: ['  █  ', '  █  ', '  █  ', '  █  ', '  █  '],
  2: ['█████', '    █', '█████', '█    ', '█████'],
  3: ['█████', '    █', '█████', '    █', '█████'],
  4: ['█   █', '█   █', '█████', '    █', '    █'],
  5: ['█████', '█    ', '█████', '    █', '█████'],
  6: ['█████', '█    ', '█████', '█   █', '█████'],
  7: ['█████', '    █', '    █', '    █', '    █'],
  8: ['█████', '█   █', '█████', '█   █', '█████'],
  9: ['█████', '█   █', '█████', '    █', '█████'],
  ':': ['     ', '  █  ', '     ', '  █  ', '     '],
  '+': ['     ', '  █  ', '█████', '  █  ', '     '],
  '-': ['     ', '     ', '█████', '     ', '     '],
  ' ': ['     ', '     ', '     ', '     ', '     '],
};

function renderBigTime(canvas, row, widthCenter, timeStr) {
  const chars = Array.from(timeStr);
  const totalWidth = chars.length * 6 - 1;
  const colStart = widthCenter - Math.floor(totalWidth / 2);

  for (let lineIdx = 0; lineIdx < 5; lineIdx++) {
    let col = colStart;
    for (const ch of chars) {
      const segment = (DIGITS[ch] || DIGITS[' '])[lineIdx];
      canvas.addstr(row + lineIdx, col, segment);
      col += 6;
    }
  }
}

function drawProgressBar(canvas, row, widthCenter, elapsed, total, width = 36) {
  const barWidth = Math.min(width, Math.max(10, canvas.cols - 14));
  const filled = total > 0 ? Math.floor((elapsed / total) * barWidth) : 0;
  const clampedFilled = Math.max(0, Math.min(filled, barWidth));
  const bar = '█'.repeat(clampedFilled) + '░'.repeat(barWidth - clampedFilled);
  const col = widthCenter - Math.floor(barWidth / 2);
  canvas.addstr(row, col, bar);
}

/**
 * Screen to choose session duration presets.
 */
export function runSessionPresetScreen(canvas, keyManager, connection) {
  return new Promise((resolve) => {
    const sessionTimes = [
      [25 * 60, 5 * 60],
      [50 * 60, 10 * 60],
      [75 * 60, 15 * 60],
      [110 * 60, 20 * 60],
    ];
    const labels = [
      '  25 min / 5 min break  ',
      '  50 min / 10 min break  ',
      '  75 min / 15 min break  ',
      '  110 min / 20 min break  ',
      '  Back  ',
    ];
    let selected = 0;

    const title = `
    ____  _____ ____ ____ ___ ___  _   _
   / ___|| ____/ ___/ ___|_ _/ _ \\| \\ | |
   \\___ \\|  _| \\___ \\___ \\| | | | |  \\| |
    ___) | |___ ___) |__) | | |_| | |\\  |
   |____/|_____|____/____/___\\___/|_| \\_|
    `;

    const render = () => {
      canvas.resize();
      canvas.clear();

      const splitTitle = title.split('\n').filter((l) => l.trim().length > 0);
      const hCenter = Math.floor(canvas.rows / 2);
      const wCenter = Math.floor(canvas.cols / 2);

      let row = Math.max(1, hCenter - splitTitle.length - 4);
      for (const line of splitTitle) {
        const col = wCenter - Math.floor(visibleLength(line) / 2);
        canvas.addstr(row, col, line);
        row++;
      }

      canvas.addstr(row + 1, wCenter - 12, '─'.repeat(24));

      const menuStartRow = row + 2;
      for (let i = 0; i < labels.length; i++) {
        const r = menuStartRow + i;
        const label = labels[i];
        const c = wCenter - Math.floor(visibleLength(label) / 2);

        if (selected === i) {
          canvas.addstr(r, c, label, (t) => style.bold(style.reverse(t)));
        } else {
          canvas.addstr(r, c, label);
        }
      }

      const hintRow = menuStartRow + labels.length + 1;
      canvas.addstr(hintRow, wCenter - 12, '─'.repeat(24));
      const hint = '↑↓ navigate   enter select';
      canvas.addstr(hintRow + 1, wCenter - Math.floor(visibleLength(hint) / 2), hint);

      canvas.flush();
    };

    render();

    const unsubscribe = keyManager.subscribe(async (str, key) => {
      if (!key) return;

      if (key.name === 'up' || str === 'k' || str === 'K') {
        selected = (selected - 1 + labels.length) % labels.length;
        render();
      } else if (key.name === 'down' || str === 'j' || str === 'J') {
        selected = (selected + 1) % labels.length;
        render();
      } else if (key.name === 'return' || key.name === 'enter') {
        if (selected === labels.length - 1) {
          unsubscribe();
          resolve();
        } else {
          unsubscribe();
          const [workDuration, breakDuration] = sessionTimes[selected];
          await runTimerScreen(canvas, keyManager, connection, workDuration, breakDuration);
          resolve();
        }
      }
    });

    const onResize = () => render();
    process.stdout.on('resize', onResize);

    const originalResolve = resolve;
    resolve = (val) => {
      process.stdout.removeListener('resize', onResize);
      originalResolve(val);
    };
  });
}

/**
 * Runs the active Pomodoro Timer Screen.
 */
export function runTimerScreen(canvas, keyManager, connection, workDuration, breakDuration) {
  return new Promise((resolve) => {
    let currentTheme = db.getSetting(connection, 'theme', 'donut');
    const { sessionId, startTime } = sess.createSession(connection, workDuration, breakDuration);

    let phase = 'WORK';
    let workEndedTime = null;
    let breakStartTime = null;
    let tickCount = 0;
    let overtimeSeconds = 0;
    let savedSession = false;
    let timerId = null;

    const cleanup = () => {
      if (timerId) clearInterval(timerId);
      if (!savedSession) {
        const now = Date.now();
        if (phase === 'WORK') {
          const elapsed = Math.round((now - startTime.getTime()) / 1000);
          sess.endSession(connection, sessionId, elapsed);
        } else if (phase === 'OVERTIME' || phase === 'BREAK') {
          const totalWork = workDuration + overtimeSeconds;
          sess.endSession(connection, sessionId, totalWork);
        }
      }
      unsubscribe();
      process.stdout.removeListener('resize', onResize);
      resolve();
    };

    const unsubscribe = keyManager.subscribe((str, key) => {
      if (!key) return;

      // Cycle theme with 't', 'T', or Tab
      if (str === 't' || str === 'T' || key.name === 'tab') {
        currentTheme = getNextTheme(currentTheme);
        db.setSetting(connection, 'theme', currentTheme);
        return;
      }

      if (phase === 'WORK') {
        if (str === 'q' || str === 'Q') {
          const elapsed = Math.round((Date.now() - startTime.getTime()) / 1000);
          sess.endSession(connection, sessionId, elapsed);
          savedSession = true;
          sess.notify('Pomodoro', 'Session stopped early.');
          cleanup();
        } else if (str === 'b' || str === 'B') {
          const elapsed = Math.round((Date.now() - startTime.getTime()) / 1000);
          sess.endSession(connection, sessionId, elapsed);
          savedSession = true;
          phase = 'BREAK';
          breakStartTime = Date.now();
          sess.notify('Pomodoro', 'Break started early.');
        }
      } else if (phase === 'OVERTIME') {
        if (str === 'q' || str === 'Q') {
          const totalWork = workDuration + overtimeSeconds;
          sess.endSession(connection, sessionId, totalWork);
          savedSession = true;
          sess.notify('Pomodoro', `Session saved: ${Math.floor(totalWork / 60)}m focused!`);
          cleanup();
        } else if (key.name === 'return' || key.name === 'enter' || str === 'b' || str === 'B' || str === ' ') {
          const totalWork = workDuration + overtimeSeconds;
          sess.endSession(connection, sessionId, totalWork);
          savedSession = true;
          phase = 'BREAK';
          breakStartTime = Date.now();
          sess.notify('Pomodoro', 'Break started. Take some rest!');
        }
      } else if (phase === 'BREAK') {
        if (str === 'q' || str === 'Q' || key.name === 'escape') {
          cleanup();
        }
      }
    });

    const onResize = () => render();
    process.stdout.on('resize', onResize);

    const render = () => {
      canvas.resize();
      canvas.clear();

      tickCount++;
      const frameIdx = Math.floor(tickCount / 2); // Frame advances every ~500ms
      const now = Date.now();
      const widthCenter = Math.floor(canvas.cols / 2);

      // --- State Transitions ---
      if (phase === 'WORK') {
        const elapsed = Math.round((now - startTime.getTime()) / 1000);
        if (elapsed >= workDuration) {
          phase = 'OVERTIME';
          workEndedTime = now;
          overtimeSeconds = 0;
          sess.notify('Pomodoro', 'Work session complete! Start break or keep going?');
          beep();
        }
      } else if (phase === 'OVERTIME') {
        if (workEndedTime) {
          overtimeSeconds = Math.round((now - workEndedTime) / 1000);
        }
      } else if (phase === 'BREAK') {
        if (breakStartTime) {
          const breakElapsed = Math.round((now - breakStartTime) / 1000);
          if (breakElapsed >= breakDuration) {
            sess.notify('Pomodoro', 'Break complete! Well done.');
            canvas.clear();
            const msg = 'Break complete! Well done.';
            canvas.addstr(Math.floor(canvas.rows / 2) - 1, widthCenter - Math.floor(msg.length / 2), msg, style.bold);
            const hint = 'Press any key to return to menu';
            canvas.addstr(Math.floor(canvas.rows / 2) + 1, widthCenter - Math.floor(hint.length / 2), hint);
            canvas.flush();
            cleanup();
            return;
          }
        }
      }

      // --- Time Strings & Progress Calculations ---
      let timeStr;
      let barElapsed;
      let barTotal;
      let progressPct;
      let pct;
      let phaseTitle;

      if (phase === 'WORK') {
        const elapsed = Math.round((now - startTime.getTime()) / 1000);
        const timeRemaining = Math.max(0, workDuration - elapsed);
        const hours = Math.floor(timeRemaining / 3600);
        const minutes = Math.floor((timeRemaining % 3600) / 60);
        const seconds = timeRemaining % 60;

        timeStr = hours > 0
          ? `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
          : `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

        barElapsed = Math.min(elapsed, workDuration);
        barTotal = workDuration;
        progressPct = workDuration > 0 ? elapsed / workDuration : 1.0;
        pct = Math.floor(progressPct * 100);
        phaseTitle = '── WORK ──';
      } else if (phase === 'OVERTIME') {
        const hours = Math.floor(overtimeSeconds / 3600);
        const minutes = Math.floor((overtimeSeconds % 3600) / 60);
        const seconds = overtimeSeconds % 60;

        timeStr = hours > 0
          ? `+${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
          : `+${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

        barElapsed = workDuration;
        barTotal = workDuration;
        progressPct = 1.0;
        pct = 100;
        phaseTitle = '── OVERTIME (+EXTRA TIME) ──';
      } else {
        const breakElapsed = breakStartTime ? Math.round((now - breakStartTime) / 1000) : 0;
        const timeRemaining = Math.max(0, breakDuration - breakElapsed);
        const hours = Math.floor(timeRemaining / 3600);
        const minutes = Math.floor((timeRemaining % 3600) / 60);
        const seconds = timeRemaining % 60;

        timeStr = hours > 0
          ? `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
          : `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

        barElapsed = Math.min(breakElapsed, breakDuration);
        barTotal = breakDuration;
        progressPct = breakDuration > 0 ? breakElapsed / breakDuration : 1.0;
        pct = Math.floor(progressPct * 100);
        phaseTitle = '── BREAK ──';
      }

      // --- Animation Frame ---
      const [animLines, animCaption] = getAnimationLines(currentTheme, phase, frameIdx, progressPct);
      const timerRequiredRows = 14;
      const availableAnimRows = Math.max(0, canvas.rows - timerRequiredRows);
      const canShowAnim = animLines.length > 0 && availableAnimRows >= 8;

      let displayLines = [];
      if (canShowAnim) {
        const maxAnimLines = availableAnimRows - (animCaption ? 1 : 0);
        if (animLines.length <= maxAnimLines) {
          displayLines = animLines;
        } else {
          const excess = animLines.length - maxAnimLines;
          const startCrop = Math.floor(excess / 2);
          displayLines = animLines.slice(startCrop, startCrop + maxAnimLines);
        }
      }

      const totalHeight = displayLines.length + (animCaption && (canShowAnim || canvas.rows >= 18) ? 1 : 0) + timerRequiredRows;
      let row = Math.max(1, Math.floor((canvas.rows - totalHeight) / 2));

      // Phase header
      canvas.addstr(row, widthCenter - Math.floor(visibleLength(phaseTitle) / 2), phaseTitle, style.bold);
      row++;

      // Animation & Caption
      if (displayLines.length > 0) {
        for (const line of displayLines) {
          canvas.addstr(row, widthCenter - Math.floor(visibleLength(line) / 2), line);
          row++;
        }
        if (animCaption) {
          canvas.addstr(row, widthCenter - Math.floor(visibleLength(animCaption) / 2), animCaption, style.dim);
          row++;
        }
      } else if (animCaption && canvas.rows >= 18) {
        canvas.addstr(row, widthCenter - Math.floor(visibleLength(animCaption) / 2), animCaption, style.dim);
        row++;
      }

      canvas.addstr(row, widthCenter - 15, '─'.repeat(30));
      row++;

      // Big Digital Clock
      renderBigTime(canvas, row, widthCenter, timeStr);
      row += 5;

      canvas.addstr(row, widthCenter - 15, '─'.repeat(30));
      row++;

      // Progress Bar & Info
      drawProgressBar(canvas, row, widthCenter, barElapsed, barTotal);
      row++;

      let statusText;
      if (phase === 'OVERTIME') {
        const extraMins = Math.floor(overtimeSeconds / 60);
        const extraSecs = overtimeSeconds % 60;
        statusText = `Work Complete! +${extraMins}m ${extraSecs}s extra counted`;
      } else {
        statusText = `${pct}%`;
      }
      canvas.addstr(row, widthCenter - Math.floor(visibleLength(statusText) / 2), statusText);
      row++;

      canvas.addstr(row, widthCenter - 15, '─'.repeat(30));
      row++;

      // Hints & Controls
      const themeName = getThemeDisplayName(currentTheme);
      if (phase === 'WORK') {
        const hints = `q stop   b take break   t theme (${themeName})`;
        canvas.addstr(row, widthCenter - Math.floor(visibleLength(hints) / 2), hints);
      } else if (phase === 'OVERTIME') {
        const prompt = 'enter / b Start Break   |   q Save & Exit';
        canvas.addstr(row, widthCenter - Math.floor(visibleLength(prompt) / 2), prompt, style.bold);
        row++;
        const themeHint = `t theme (${themeName})`;
        canvas.addstr(row, widthCenter - Math.floor(visibleLength(themeHint) / 2), themeHint);
      } else {
        const hints = `q finish break   t theme (${themeName})`;
        canvas.addstr(row, widthCenter - Math.floor(visibleLength(hints) / 2), hints);
      }

      canvas.flush();
    };

    render();
    timerId = setInterval(render, 250);
  });
}
