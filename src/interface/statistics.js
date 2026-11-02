import * as db from '../db.js';
import { style, visibleLength, fmtDuration, fmtDurationShort } from '../utils.js';

const TITLE = `
 ___ _____  _  _____ ___ 
/ __|_   _|/_\\|_   _/ __|
\\__ \\ | | / _ \\ | | \\__ \\
|___/ |_|/_/ \\_\\|_| |___/
`;

function drawHorizontalBars(canvas, startRow, widthCenter, stats, scaleSeconds, barMax = 28) {
  const dowAbbrs = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  for (let i = 0; i < stats.length; i++) {
    const [dateStr, seconds] = stats[i];
    const dObj = new Date(dateStr + 'T00:00:00');
    // In JS Date, getDay() returns 0 for Sunday, 1 for Monday...
    const dowIdx = (dObj.getDay() + 6) % 7; // Convert to 0 for Monday.. 6 for Sunday
    const dow = dowAbbrs[dowIdx];

    const filled = scaleSeconds > 0 ? Math.floor((seconds / scaleSeconds) * barMax) : 0;
    const clampedFilled = Math.max(0, Math.min(filled, barMax));
    const bar = '█'.repeat(clampedFilled) + '░'.repeat(barMax - clampedFilled);

    const dayLabel = `${dateStr.slice(5)} (${dow})`;
    const durStr = fmtDuration(seconds).padStart(7, ' ');
    const line = `  ${dayLabel}  ${bar}  ${durStr}`;

    canvas.addstr(startRow + i, widthCenter - Math.floor((barMax + 24) / 2), line);
  }
}

function renderBarsView(canvas, row, widthCenter, dailyStats, rollingStats) {
  canvas.addstr(row, widthCenter - 12, 'LAST 7 DAYS (BARS)', style.bold);
  row++;

  const maxVal = Math.max(0, ...dailyStats.map((s) => s[1]));
  const dailyScale = Math.max(maxVal, 8 * 3600);

  drawHorizontalBars(canvas, row, widthCenter, dailyStats, dailyScale);
  row += dailyStats.length;

  canvas.addstr(row, widthCenter - 22, '─'.repeat(44));
  row++;

  canvas.addstr(row, widthCenter - 20, 'ROLLING TOTALS', style.bold);
  row++;

  const [last7, last14, last21, last28] = rollingStats;
  const periods = [
    ['Last  7 days', last7],
    ['Last 14 days', last14],
    ['Last 21 days', last21],
    ['Last 28 days', last28],
  ];

  const periodScales = [7, 14, 21, 28];
  for (let i = 0; i < periods.length; i++) {
    const [label, seconds] = periods[i];
    const nDays = periodScales[i];
    const scale = Math.max(nDays * dailyScale, 1);
    const filled = Math.max(0, Math.min(28, Math.floor((seconds / scale) * 28)));
    const bar = '█'.repeat(filled) + '░'.repeat(28 - filled);
    const durStr = fmtDuration(seconds).padStart(7, ' ');
    const line = `  ${label}  ${bar}  ${durStr}`;

    canvas.addstr(row, widthCenter - Math.floor((28 + 24) / 2), line);
    row++;
  }

  return row;
}

function renderHistogramView(canvas, row, widthCenter, dailyStats) {
  canvas.addstr(row, widthCenter - 14, 'WEEKLY COLUMN HISTOGRAM', style.bold);
  row++;

  const chronoStats = [...dailyStats].reverse();
  const maxVal = Math.max(0, ...chronoStats.map((s) => s[1]));
  const maxSec = Math.max(maxVal, 3600);
  const chartHeight = 6;

  const dowAbbrs = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  const colWidth = 5;
  const chartContentWidth = 7 * colWidth + 8;
  const chartStartCol = widthCenter - Math.floor(chartContentWidth / 2);

  for (let lvl = chartHeight - 1; lvl >= 0; lvl--) {
    const threshFull = (lvl + 0.65) / chartHeight;
    const threshHalf = (lvl + 0.20) / chartHeight;

    let yLabel;
    if (lvl === chartHeight - 1) {
      yLabel = fmtDurationShort(maxSec).padStart(5, ' ');
    } else if (lvl === Math.floor(chartHeight / 2)) {
      yLabel = fmtDurationShort(Math.floor(maxSec / 2)).padStart(5, ' ');
    } else if (lvl === 0) {
      yLabel = '   0m';
    } else {
      yLabel = '     ';
    }

    let barLine = `${yLabel} │ `;
    for (const [, sec] of chronoStats) {
      const frac = maxSec > 0 ? sec / maxSec : 0;
      let segment;
      if (frac >= threshFull) {
        segment = ' ███ ';
      } else if (frac >= threshHalf) {
        segment = ' ▄▄▄ ';
      } else {
        segment = '     ';
      }
      barLine += segment;
    }

    canvas.addstr(row, chartStartCol, barLine);
    row++;
  }

  // Baseline axis
  const axisLine = '      └' + '─────'.repeat(7);
  canvas.addstr(row, chartStartCol, axisLine);
  row++;

  // Day of week labels
  let dowLine = '        ';
  for (const [dateStr] of chronoStats) {
    const dObj = new Date(dateStr + 'T00:00:00');
    const dow = dowAbbrs[(dObj.getDay() + 6) % 7];
    dowLine += ` ${dow}  `;
  }
  canvas.addstr(row, chartStartCol, dowLine);
  row++;

  // Date labels
  let dateLine = '        ';
  for (const [dateStr] of chronoStats) {
    const mmdd = dateStr.slice(5).replace('-', '/');
    dateLine += `${mmdd} `;
  }
  canvas.addstr(row, chartStartCol, dateLine, style.dim);
  row++;

  // Duration labels
  let durLine = '        ';
  for (const [, sec] of chronoStats) {
    const dStr = fmtDurationShort(sec).padStart(4, ' ').padEnd(5, ' ');
    durLine += dStr;
  }
  canvas.addstr(row, chartStartCol, durLine, style.bold);
  row++;

  canvas.addstr(row, widthCenter - 22, '─'.repeat(44));
  row++;

  // Summary
  const total7d = chronoStats.reduce((acc, s) => acc + s[1], 0);
  const dailyAvg = Math.floor(total7d / 7);
  const summary = `7-Day Total: ${fmtDuration(total7d)}  •  Daily Avg: ${fmtDuration(dailyAvg)}`;
  canvas.addstr(row, widthCenter - Math.floor(visibleLength(summary) / 2), summary);
  row++;

  return row;
}

function renderHeatmapView(canvas, row, widthCenter, connection) {
  canvas.addstr(row, widthCenter - 15, '4-WEEK FOCUS HEATMAP & STREAKS', style.bold);
  row++;

  const heatmapData = db.getHeatmapData(connection, 4);
  const [curStreak, bestStreak] = db.getStreaks(connection);
  const statsMap = new Map(heatmapData.map(([d, sec]) => [d, sec]));

  const today = new Date();
  const dowIdx = (today.getDay() + 6) % 7; // Monday = 0
  const startOfThisWeek = new Date(today);
  startOfThisWeek.setDate(startOfThisWeek.getDate() - dowIdx);

  const startDate = new Date(startOfThisWeek);
  startDate.setDate(startDate.getDate() - 21); // 3 weeks prior

  const dowLabels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  const tableStartCol = widthCenter - 16;

  const header = '       Wk-3  Wk-2  Wk-1  This';
  canvas.addstr(row, tableStartCol, header, style.dim);
  row++;

  const todayStr = today.toISOString().slice(0, 10);

  for (let d = 0; d < 7; d++) {
    let line = `  ${dowLabels[d]}  `;
    for (let w = 0; w < 4; w++) {
      const curDate = new Date(startDate);
      curDate.setDate(curDate.getDate() + w * 7 + d);
      const curStr = curDate.toISOString().slice(0, 10);

      if (curStr > todayStr) {
        line += ' ·  ';
      } else {
        const sec = statsMap.get(curStr) || 0;
        if (sec === 0) {
          line += ' ░  ';
        } else if (sec < 1800) {
          line += ' ▒  ';
        } else if (sec < 3600) {
          line += ' ▓  ';
        } else {
          line += ' █  ';
        }
      }
    }
    canvas.addstr(row, tableStartCol, line);
    row++;
  }

  canvas.addstr(row, widthCenter - 22, '─'.repeat(44));
  row++;

  const legend = 'Legend: ░ 0m   ▒ <30m   ▓ 30-60m   █ 1h+';
  canvas.addstr(row, widthCenter - Math.floor(visibleLength(legend) / 2), legend, style.dim);
  row++;

  const total28d = heatmapData.reduce((acc, s) => acc + s[1], 0);
  const activeDays = heatmapData.filter((s) => s[1] > 0).length;
  const monthSummary = `Past 28 Days: ${fmtDuration(total28d)}  •  Active: ${activeDays}/28 days`;
  canvas.addstr(row, widthCenter - Math.floor(visibleLength(monthSummary) / 2), monthSummary);
  row++;

  const streaksText = `🔥 Current Streak: ${curStreak} days   ★ Best Streak: ${bestStreak} days`;
  canvas.addstr(row, widthCenter - Math.floor(visibleLength(streaksText) / 2), streaksText, style.bold);
  row++;

  return row;
}

function renderRecordsView(canvas, row, widthCenter, connection) {
  canvas.addstr(row, widthCenter - 13, 'LIFETIME RECORDS & RANK', style.bold);
  row++;

  const stats = db.getLifetimeStats(connection);
  const [curStreak, bestStreak] = db.getStreaks(connection);

  const totalSec = stats.total_seconds;
  let rankTitle;
  if (totalSec < 5 * 3600) {
    rankTitle = 'Apprentice Novice ✦';
  } else if (totalSec < 20 * 3600) {
    rankTitle = 'Journeyman Adept ⚔';
  } else if (totalSec < 50 * 3600) {
    rankTitle = 'Master of Focus 🛡';
  } else {
    rankTitle = 'Grandmaster Archmage 👑';
  }

  const cardWidth = 46;
  const cardStartCol = widthCenter - Math.floor(cardWidth / 2);

  canvas.addstr(row, cardStartCol, `┌${'─'.repeat(cardWidth - 2)}┐`);
  row++;

  const rankLine = `  Rank: ${rankTitle}`;
  canvas.addstr(row, cardStartCol, `│${rankLine.padEnd(cardWidth - 2, ' ')}│`, style.bold);
  row++;

  canvas.addstr(row, cardStartCol, `├${'─'.repeat(cardWidth - 2)}┤`);
  row++;

  const items = [
    `  ⏱  Total Focus Time:       ${fmtDuration(stats.total_seconds)}`,
    `  🎯 Completed Sessions:     ${stats.total_count} sessions`,
    `  🏆 Longest Session:        ${fmtDuration(stats.max_seconds)}`,
    `  ⏳ Average Session:        ${fmtDuration(stats.avg_seconds)}`,
    `  📅 Today's Focus:          ${fmtDuration(stats.today_seconds)} (${stats.today_count} sessions)`,
    `  🌟 Top Day of Week:        ${stats.best_day[0]} (${fmtDuration(stats.best_day[1])})`,
    `  🔥 Current Daily Streak:   ${curStreak} days`,
    `  ★  All-Time Best Streak:   ${bestStreak} days`,
  ];

  for (const item of items) {
    canvas.addstr(row, cardStartCol, `│${item.padEnd(cardWidth - 2, ' ')}│`);
    row++;
  }

  canvas.addstr(row, cardStartCol, `└${'─'.repeat(cardWidth - 2)}┘`);
  row++;

  return row;
}

/**
 * Runs the Statistics Screen with tabbed navigation.
 */
export function runStatisticsScreen(canvas, keyManager, connection) {
  return new Promise((resolve) => {
    const tabNames = ['1: Bars', '2: Columns', '3: Heatmap', '4: Records'];

    const savedViewStr = db.getSetting(connection, 'stats_view', '0');
    let activeView = parseInt(savedViewStr, 10);
    if (isNaN(activeView) || activeView < 0 || activeView > 3) {
      activeView = 0;
    }

    const render = () => {
      canvas.resize();
      canvas.clear();

      const widthCenter = Math.floor(canvas.cols / 2);

      if (canvas.rows < 18 || canvas.cols < 46) {
        const msg = 'Window too small for statistics';
        const hint = "Resize window or press 'q' to go back";
        canvas.addstr(Math.floor(canvas.rows / 2) - 1, widthCenter - Math.floor(msg.length / 2), msg, style.bold);
        canvas.addstr(Math.floor(canvas.rows / 2) + 1, widthCenter - Math.floor(hint.length / 2), hint);
        canvas.flush();
        return;
      }

      const dailyStats = db.getSessionStatsDaily(connection);
      const rollingStats = db.getSessionStatsWeekly(connection);

      const splitTitle = TITLE.split('\n').filter((l) => l.trim().length > 0);
      const totalContentRows = 22;
      let row = canvas.rows >= 23 ? Math.max(1, Math.floor((canvas.rows - totalContentRows) / 2)) : 0;

      for (const line of splitTitle) {
        canvas.addstr(row, widthCenter - Math.floor(visibleLength(line) / 2), line);
        row++;
      }

      // Tab Bar
      let currentCol = widthCenter - 22;
      for (let i = 0; i < tabNames.length; i++) {
        const label = ` ${tabNames[i]} `;
        if (i === activeView) {
          canvas.addstr(row, currentCol, label, (t) => style.bold(style.reverse(t)));
        } else {
          canvas.addstr(row, currentCol, label, style.dim);
        }
        currentCol += label.length + 2;
      }
      row++;

      canvas.addstr(row, widthCenter - 22, '─'.repeat(44));
      row++;

      // Render Active View
      if (activeView === 0) {
        row = renderBarsView(canvas, row, widthCenter, dailyStats, rollingStats);
      } else if (activeView === 1) {
        row = renderHistogramView(canvas, row, widthCenter, dailyStats);
      } else if (activeView === 2) {
        row = renderHeatmapView(canvas, row, widthCenter, connection);
      } else if (activeView === 3) {
        row = renderRecordsView(canvas, row, widthCenter, connection);
      }

      // Footer
      canvas.addstr(row, widthCenter - 22, '─'.repeat(44));
      row++;
      const hint = '←/→ / Tab switch view   1-4 jump   q back';
      canvas.addstr(row, widthCenter - Math.floor(visibleLength(hint) / 2), hint);

      canvas.flush();
    };

    render();

    const unsubscribe = keyManager.subscribe((str, key) => {
      if (!key) return;

      if (str === 'q' || str === 'Q' || key.name === 'escape') {
        unsubscribe();
        resolve();
      } else if (key.name === 'right' || str === 'l' || str === 'L' || key.name === 'tab') {
        activeView = (activeView + 1) % 4;
        db.setSetting(connection, 'stats_view', String(activeView));
        render();
      } else if (key.name === 'left' || str === 'h' || str === 'H') {
        activeView = (activeView - 1 + 4) % 4;
        db.setSetting(connection, 'stats_view', String(activeView));
        render();
      } else if (str === '1') {
        activeView = 0;
        db.setSetting(connection, 'stats_view', String(activeView));
        render();
      } else if (str === '2') {
        activeView = 1;
        db.setSetting(connection, 'stats_view', String(activeView));
        render();
      } else if (str === '3') {
        activeView = 2;
        db.setSetting(connection, 'stats_view', String(activeView));
        render();
      } else if (str === '4') {
        activeView = 3;
        db.setSetting(connection, 'stats_view', String(activeView));
        render();
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
