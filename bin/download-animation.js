#!/usr/bin/env node

/**
 * CLI utility to download pieces directly from ascii.rest into src/interface/pieces/
 *
 * Usage:
 *   node bin/download-animation.js --list
 *   node bin/download-animation.js <piece-name>
 */

import { execSync } from 'node:child_process';
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PIECES_DIR = join(__dirname, '../src/interface/pieces');

const pieceName = process.argv[2];

if (!pieceName || pieceName === '--help' || pieceName === '-h') {
  console.log(`
ascii.rest Animation Downloader
Download ASCII animations directly from ascii.rest into pomodoro-cli.

Usage:
  node bin/download-animation.js --list        List available pieces
  node bin/download-animation.js <piece-name> Download a specific piece

Example:
  node bin/download-animation.js butterfly
`);
  process.exit(0);
}

if (pieceName === '--list' || pieceName === 'list') {
  console.log('Fetching available pieces from ascii.rest...\n');
  try {
    const listOut = execSync('npx -y ascii.rest list', { encoding: 'utf8' });
    console.log(listOut);
  } catch (err) {
    console.error('Failed to list pieces:', err.message);
  }
  process.exit(0);
}

console.log(`Downloading "${pieceName}" from ascii.rest...`);
try {
  // Use npm pack or npx to fetch the piece file
  const tmpDir = `/tmp/ascii-dl-${Date.now()}`;
  mkdirSync(tmpDir, { recursive: true });
  execSync(`npm pack ascii.rest && tar -xzf *.tgz`, { cwd: tmpDir, stdio: 'ignore' });

  const srcFile = join(tmpDir, `package/dist/pieces/${pieceName}.js`);
  if (!existsSync(srcFile)) {
    console.error(`Error: Piece "${pieceName}" not found in ascii.rest.`);
    process.exit(1);
  }

  mkdirSync(PIECES_DIR, { recursive: true });
  const destFile = join(PIECES_DIR, `${pieceName}.js`);
  execSync(`cp "${srcFile}" "${destFile}"`);

  console.log(`Successfully downloaded "${pieceName}" to ${destFile}`);
  console.log(`You can now register it in src/interface/animations.js!`);
} catch (err) {
  console.error(`Failed to download piece: ${err.message}`);
  process.exit(1);
}
