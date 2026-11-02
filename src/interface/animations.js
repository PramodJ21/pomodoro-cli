// Animated ASCII companion themes powered by ascii.rest (https://ascii.rest)
// All pieces are self-contained mathematical & artistic terminal animations.

import * as donutMod from './pieces/donut.js';
import * as catMod from './pieces/cat.js';
import * as campfireMod from './pieces/campfire.js';
import * as coffeeMod from './pieces/coffee.js';
import * as hourglassMod from './pieces/hourglass.js';
import * as cubeMod from './pieces/cube.js';
import * as matrixMod from './pieces/matrix-rain.js';
import * as starfieldMod from './pieces/starfield.js';
import * as ballsMod from './pieces/bouncing-balls.js';
import * as candleMod from './pieces/candle.js';
import * as moonMod from './pieces/moon-phases.js';
import * as dnaMod from './pieces/dna-helix.js';
import * as firefliesMod from './pieces/fireflies.js';
import * as galaxyMod from './pieces/galaxy.js';
import * as foxMod from './pieces/fox.js';
import * as doomFireMod from './pieces/doom-fire.js';
import * as snakeMod from './pieces/snake.js';
import * as owlMod from './pieces/owl.js';
import * as seaSwellMod from './pieces/sea-swell.js';

export const THEMES = [
  'donut',
  'cat',
  'campfire',
  'coffee',
  'hourglass',
  'cube',
  'matrix-rain',
  'starfield',
  'bouncing-balls',
  'candle',
  'moon-phases',
  'dna-helix',
  'fireflies',
  'galaxy',
  'fox',
  'doom-fire',
  'snake',
  'owl',
  'sea-swell',
  'none',
];

export const THEME_NAMES = {
  donut: 'Donut 3D',
  cat: 'Sleeping Cat',
  campfire: 'Cozy Campfire',
  coffee: 'Steaming Coffee',
  hourglass: 'Hourglass',
  cube: 'Wireframe Cube',
  'matrix-rain': 'Matrix Rain',
  starfield: 'Warp Starfield',
  'bouncing-balls': 'Bouncing Balls',
  candle: 'Candle Flame',
  'moon-phases': 'Moon Phases',
  'dna-helix': 'DNA Double Helix',
  fireflies: 'Fireflies',
  galaxy: 'Spiral Galaxy',
  fox: 'Sleeping Fox',
  'doom-fire': 'Doom Fire',
  snake: 'Slithering Snake',
  owl: 'Night Owl',
  'sea-swell': 'Ocean Swell',
  none: 'Off',
};

// Aliases to seamlessly migrate old theme IDs stored in database
const LEGACY_ALIASES = {
  bonfire: 'campfire',
  matrix: 'matrix-rain',
  stars: 'starfield',
  moon: 'moon-phases',
  clock: 'donut',
  duck: 'cat',
  knight: 'cube',
  mage: 'galaxy',
  slime: 'bouncing-balls',
};

// Piece registry mapping theme ID to loader and metadata
const PIECES = {
  donut: { mod: donutMod, caption: 'Rotating Donut (donut.c)' },
  cat: { mod: catMod, caption: 'Tabby asleep on paws' },
  campfire: { mod: campfireMod, caption: 'Flickering Campfire' },
  coffee: { mod: coffeeMod, caption: 'Steaming Coffee' },
  hourglass: { mod: hourglassMod, caption: 'Sands of Time' },
  cube: { mod: cubeMod, caption: '3D Wireframe Cube' },
  'matrix-rain': { mod: matrixMod, caption: 'Falling Matrix Code' },
  starfield: { mod: starfieldMod, caption: 'Cosmic Warp Speed' },
  'bouncing-balls': { mod: ballsMod, caption: 'Bouncing Balls' },
  candle: { mod: candleMod, caption: 'Candle Flame' },
  'moon-phases': { mod: moonMod, caption: 'Lunar Moon Phases' },
  'dna-helix': { mod: dnaMod, caption: 'DNA Double Helix' },
  fireflies: { mod: firefliesMod, caption: 'Fireflies Swarm' },
  galaxy: { mod: galaxyMod, caption: 'Spiral Galaxy' },
  fox: { mod: foxMod, caption: 'Sleeping Fox' },
  'doom-fire': { mod: doomFireMod, caption: 'PSX Doom Fire' },
  snake: { mod: snakeMod, caption: 'Slithering Snake' },
  owl: { mod: owlMod, caption: 'Observing Night Owl' },
  'sea-swell': { mod: seaSwellMod, caption: 'Ocean Sailboat Swell' },
};

// Cached renderer instances (one instance per theme)
const RENDERER_INSTANCES = new Map();

function getRenderer(theme) {
  if (RENDERER_INSTANCES.has(theme)) {
    return RENDERER_INSTANCES.get(theme);
  }
  const entry = PIECES[theme];
  if (!entry || !entry.mod || !entry.mod.default) {
    return null;
  }
  const renderer = entry.mod.default();
  RENDERER_INSTANCES.set(theme, renderer);
  return renderer;
}

export function resolveTheme(theme) {
  if (!theme) return 'donut';
  const aliased = LEGACY_ALIASES[theme] || theme;
  return THEMES.includes(aliased) ? aliased : 'donut';
}

export function getNextTheme(current) {
  const resolved = resolveTheme(current);
  const idx = THEMES.indexOf(resolved);
  const nextIdx = (idx + 1) % THEMES.length;
  return THEMES[nextIdx];
}

export function getThemeDisplayName(theme) {
  const resolved = resolveTheme(theme);
  return THEME_NAMES[resolved] || resolved;
}

/**
 * Trims leading and trailing rows that are completely empty / whitespace.
 * Preserves the uniform width of internal lines.
 */
function trimBlankRows(lines) {
  let start = 0;
  while (start < lines.length && lines[start].trim() === '') {
    start++;
  }
  let end = lines.length - 1;
  while (end >= start && lines[end].trim() === '') {
    end--;
  }
  if (start > end) return [];
  return lines.slice(start, end + 1);
}

/**
 * Generates the ASCII animation lines and caption for a given theme, phase, and time.
 * Returns [lines: string[], caption: string]
 */
export function getAnimationLines(theme, phase, tOrFrameIdx = 0.0, progressPct = 0.0) {
  const resolved = resolveTheme(theme);
  if (resolved === 'none') {
    return [[], ''];
  }

  const piece = PIECES[resolved];
  if (!piece) {
    return [[], ''];
  }

  const renderer = getRenderer(resolved);
  if (!renderer) {
    return [[], ''];
  }

  // Continuous seconds t: either direct seconds float, or frame index
  const t = Math.max(0, typeof tOrFrameIdx === 'number' ? tOrFrameIdx : 0);
  let rawFrame = '';
  try {
    rawFrame = renderer(t);
  } catch {
    return [[], ''];
  }

  const rawLines = typeof rawFrame === 'string' ? rawFrame.split('\n') : [];
  const lines = trimBlankRows(rawLines);

  // Caption based on phase
  let caption = `~ ${piece.caption} ~`;
  if (phase === 'OVERTIME') {
    caption = `~ ${piece.caption} • Overtime ~`;
  } else if (phase === 'BREAK') {
    caption = `~ ${piece.caption} • Rest & Recharge ~`;
  }

  return [lines, caption];
}
