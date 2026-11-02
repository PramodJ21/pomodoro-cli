import readline from 'node:readline';

// --- ANSI Styling ---
export const style = {
  bold: (t) => `\x1b[1m${t}\x1b[22m`,
  dim: (t) => `\x1b[2m${t}\x1b[22m`,
  reverse: (t) => `\x1b[7m${t}\x1b[27m`,
  cyan: (t) => `\x1b[36m${t}\x1b[39m`,
  yellow: (t) => `\x1b[33m${t}\x1b[39m`,
  green: (t) => `\x1b[32m${t}\x1b[39m`,
  red: (t) => `\x1b[31m${t}\x1b[39m`,
  reset: '\x1b[0m',
};

export function visibleLength(str) {
  // Strip ANSI escape codes to measure true printed width
  // eslint-disable-next-line no-control-regex
  return str.replace(/\x1b\[[0-9;]*m/g, '').length;
}

export function fmtDuration(seconds) {
  const s = Math.max(0, Math.floor(seconds));
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  if (h > 0) {
    return `${h}h ${String(m).padStart(2, '0')}m`;
  }
  return `${m}m`;
}

export function fmtDurationShort(seconds) {
  const s = Math.max(0, Math.floor(seconds));
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  if (h > 0 && m > 0) return `${h}h${m}m`;
  if (h > 0) return `${h}h`;
  return `${m}m`;
}

export function enterAltScreen() {
  process.stdout.write('\x1b[?1049h\x1b[?25l');
}

export function exitAltScreen() {
  process.stdout.write('\x1b[?25h\x1b[?1049l');
}

export function beep() {
  process.stdout.write('\x07');
}

/**
 * Lightweight in-memory double-buffer screen.
 * Avoids any terminal flickering by composing the whole frame and writing it in one pass.
 */
export class TerminalCanvas {
  constructor() {
    this.rows = process.stdout.rows || 24;
    this.cols = process.stdout.columns || 80;
    this.commands = [];
  }

  resize() {
    this.rows = process.stdout.rows || 24;
    this.cols = process.stdout.columns || 80;
  }

  clear() {
    this.commands = [];
  }

  addstr(row, col, text, styling = null) {
    const r = Math.floor(row);
    const c = Math.floor(col);

    if (r < 0 || r >= this.rows || c >= this.cols) {
      return;
    }

    let output = text;
    let startCol = c;

    if (startCol < 0) {
      output = output.slice(-startCol);
      startCol = 0;
    }

    const visLen = visibleLength(output);
    if (startCol + visLen > this.cols) {
      output = output.slice(0, Math.max(0, this.cols - startCol));
    }

    if (!output) return;

    if (styling) {
      output = styling(output);
    }

    // Cursor position is 1-indexed in ANSI escape sequences
    this.commands.push(`\x1b[${r + 1};${startCol + 1}H${output}`);
  }

  flush() {
    // Clear screen and draw all positioned strings
    const buffer = '\x1b[2J\x1b[H' + this.commands.join('') + style.reset;
    process.stdout.write(buffer);
  }
}

/**
 * KeyManager handles raw mode keyboard events.
 */
export class KeyManager {
  constructor() {
    this.handlers = new Set();
    this.isRaw = false;

    if (process.stdin.isTTY) {
      readline.emitKeypressEvents(process.stdin);
      process.stdin.setRawMode(true);
      this.isRaw = true;

      this.onKeypress = (str, key) => {
        // Global Ctrl+C handler
        if (key && key.ctrl && key.name === 'c') {
          exitAltScreen();
          process.exit(0);
        }

        for (const handler of this.handlers) {
          handler(str, key);
        }
      };

      process.stdin.on('keypress', this.onKeypress);
      process.stdin.resume();
    }
  }

  subscribe(handler) {
    this.handlers.add(handler);
    return () => this.handlers.delete(handler);
  }

  cleanup() {
    if (this.isRaw && process.stdin.isTTY) {
      process.stdin.removeListener('keypress', this.onKeypress);
      try {
        process.stdin.setRawMode(false);
      } catch {}
      process.stdin.pause();
    }
  }
}
