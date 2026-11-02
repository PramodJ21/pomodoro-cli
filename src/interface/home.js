import * as db from '../db.js';
import { style, visibleLength } from '../utils.js';
import { getNextTheme, getThemeDisplayName } from './animations.js';

const TITLE = `
    ____   ___  __  __  ___  ____   ___  ____   ___
   |  _ \\ / _ \\|  \\/  |/ _ \\|  _ \\ / _ \\|  _ \\ / _ \\
   | |_) | | | | |\\/| | | | | | | | | | | |_) | | | |
   |  __/| |_| | |  | | |_| | |_| | |_| |  _ <| |_| |
   |_|    \\___/|_|  |_|\\___/|____/ \\___/|_| \\_\\\\___/
`;

/**
 * Runs the Home Menu Screen.
 * Resolves with 'session', 'statistics', or 'exit'.
 */
export function runHomeScreen(canvas, keyManager, connection) {
  return new Promise((resolve) => {
    let selected = 0;
    let currentTheme = db.getSetting(connection, 'theme', 'donut');

    const render = () => {
      canvas.resize();
      canvas.clear();

      const themeDisplay = getThemeDisplayName(currentTheme);
      const options = [
        'Start Session',
        'Show Statistics',
        `Theme: ${themeDisplay}`,
        'Exit',
      ];

      const splitTitle = TITLE.split('\n').filter((l) => l.trim().length > 0);
      const hCenter = Math.floor(canvas.rows / 2);
      const wCenter = Math.floor(canvas.cols / 2);

      let row = Math.max(1, hCenter - splitTitle.length - 3);

      for (const line of splitTitle) {
        const col = wCenter - Math.floor(visibleLength(line) / 2);
        canvas.addstr(row, col, line);
        row++;
      }

      canvas.addstr(row + 1, wCenter - 14, '─'.repeat(28));

      const menuRow = row + 2;
      for (let i = 0; i < options.length; i++) {
        const r = menuRow + i;
        const label = `  ${options[i]}  `;
        const col = wCenter - Math.floor(visibleLength(label) / 2);

        if (selected === i) {
          canvas.addstr(r, col, label, (t) => style.bold(style.reverse(t)));
        } else {
          canvas.addstr(r, col, label);
        }
      }

      const hintRow = menuRow + options.length + 1;
      canvas.addstr(hintRow, wCenter - 14, '─'.repeat(28));
      const hint = '↑↓ navigate   enter select   t theme';
      canvas.addstr(hintRow + 1, wCenter - Math.floor(visibleLength(hint) / 2), hint);

      canvas.flush();
    };

    render();

    const unsubscribe = keyManager.subscribe((str, key) => {
      if (!key) return;

      if (key.name === 'up' || str === 'k' || str === 'K') {
        selected = (selected - 1 + 4) % 4;
        render();
      } else if (key.name === 'down' || str === 'j' || str === 'J') {
        selected = (selected + 1) % 4;
        render();
      } else if (str === 't' || str === 'T' || key.name === 'tab') {
        currentTheme = getNextTheme(currentTheme);
        db.setSetting(connection, 'theme', currentTheme);
        render();
      } else if (key.name === 'return' || key.name === 'enter') {
        if (selected === 0) {
          unsubscribe();
          resolve('session');
        } else if (selected === 1) {
          unsubscribe();
          resolve('statistics');
        } else if (selected === 2) {
          currentTheme = getNextTheme(currentTheme);
          db.setSetting(connection, 'theme', currentTheme);
          render();
        } else if (selected === 3) {
          unsubscribe();
          resolve('exit');
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
