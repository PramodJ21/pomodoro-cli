#!/usr/bin/env node

import { createRequire } from 'node:module';
import * as db from '../src/db.js';
import { TerminalCanvas, KeyManager, enterAltScreen, exitAltScreen } from '../src/utils.js';
import { runHomeScreen } from '../src/interface/home.js';
import { runSessionPresetScreen } from '../src/interface/session.js';
import { runStatisticsScreen } from '../src/interface/statistics.js';

const require = createRequire(import.meta.url);
const pkg = require('../package.json');

// Check CLI flags
const args = process.argv.slice(2);
if (args.includes('-v') || args.includes('--version')) {
  console.log(`pomodoro-cli v${pkg.version}`);
  process.exit(0);
}

if (args.includes('-h') || args.includes('--help')) {
  console.log(`
pomodoro-cli v${pkg.version}
A beautiful terminal Pomodoro timer with animated ASCII companions and statistics.

Usage:
  pomodoro-cli          Launch the interactive terminal interface
  pomodoro              Alias for pomodoro-cli

Controls:
  ↑/↓, k/j              Navigate menus
  Enter                 Select option
  t                     Cycle animation theme
  q                     Quit or back
  Ctrl+C                Exit anytime

Options:
  -v, --version         Show version
  -h, --help            Show this help message
`);
  process.exit(0);
}

// Ensure TTY
if (!process.stdin.isTTY || !process.stdout.isTTY) {
  console.error('pomodoro-cli requires an interactive terminal (TTY).');
  process.exit(1);
}

let cleanedUp = false;
let keyManager = null;
let conn = null;

function cleanup() {
  if (cleanedUp) return;
  cleanedUp = true;
  if (keyManager) {
    keyManager.cleanup();
  }
  exitAltScreen();
  if (conn) {
    try {
      conn.close();
    } catch {}
  }
}

process.on('SIGINT', () => {
  cleanup();
  process.exit(0);
});

process.on('SIGTERM', () => {
  cleanup();
  process.exit(0);
});

process.on('uncaughtException', (err) => {
  cleanup();
  console.error('An unexpected error occurred:');
  console.error(err);
  process.exit(1);
});

process.on('unhandledRejection', (reason) => {
  cleanup();
  console.error('Unhandled rejection:');
  console.error(reason);
  process.exit(1);
});

async function main() {
  conn = db.getConnection();
  db.initializeDb(conn);

  enterAltScreen();
  const canvas = new TerminalCanvas();
  keyManager = new KeyManager();

  while (true) {
    const choice = await runHomeScreen(canvas, keyManager, conn);
    if (choice === 'session') {
      await runSessionPresetScreen(canvas, keyManager, conn);
    } else if (choice === 'statistics') {
      await runStatisticsScreen(canvas, keyManager, conn);
    } else if (choice === 'exit') {
      break;
    }
  }

  cleanup();
  process.exit(0);
}

main().catch((err) => {
  cleanup();
  console.error(err);
  process.exit(1);
});
