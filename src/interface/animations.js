/**
 * ASCII and pixel animations for Pomodoro timer.
 * Includes inspirations from ascii-magic-art and dynamic algorithmic generators.
 */

export const THEMES = [
  'bonfire',
  'coffee',
  'cat',
  'duck',
  'knight',
  'candle',
  'matrix',
  'stars',
  'moon',
  'clock',
  'mage',
  'slime',
  'hourglass',
  'none',
];

export const THEME_NAMES = {
  bonfire: 'Bonfire',
  coffee: 'Coffee Mug',
  cat: 'Coding Cat',
  duck: 'Debug Duck',
  knight: 'Pixel Knight',
  candle: 'Candle Flame',
  matrix: 'Matrix Rain',
  stars: 'Cosmic Stars',
  moon: 'Lunar Phases',
  clock: 'Analog Clock',
  mage: 'Arcane Mage',
  slime: 'RPG Slime',
  hourglass: 'Hourglass',
  none: 'Off',
};

// --- THEME 1: Bonfire (Dark Souls coiled sword & flame) ---
const BONFIRE_WORK = [
  [
    '    (  . )    ',
    '  (  ) )  )   ',
    ' (  ) ) (  )  ',
    '   |====|     ',
    ' _/_||_\\_\\_   ',
  ],
  [
    '  ( *  )      ',
    ' ( ) (  )     ',
    '( ) ( )  )    ',
    '   |====|     ',
    ' _/_||_\\_\\_   ',
  ],
  [
    '    (  . )    ',
    '  (  ( ) )    ',
    ' ( ) (  ) )   ',
    '   |====|     ',
    ' _/_||_\\_\\_   ',
  ],
  [
    '    (   * )   ',
    '   ) ( (  )   ',
    '  ( ) ) (  )  ',
    '   |====|     ',
    ' _/_||_\\_\\_   ',
  ],
];

const BONFIRE_REST = [
  [
    '     .   *    ',
    '    ( · )     ',
    '   (  .  )    ',
    '   |====|     ',
    ' _/_||_\\_\\_   ',
  ],
  [
    '    *   .     ',
    '     ( · )    ',
    '    (  .  )   ',
    '   |====|     ',
    ' _/_||_\\_\\_   ',
  ],
];

// --- THEME 2: Coffee Mug (from ascii-magic-art coffee-steam & yawning-coffee-cup) ---
const COFFEE_WORK = [
  [
    '      ( ~ )  .   ',
    '     .  ( * )    ',
    '   ┌───────────┐ ',
    '   │  ( •‿• )  │)',
    '   │  |     |  │/',
    '   └───\\___/───┘ ',
  ],
  [
    '     ( * )  ~    ',
    '        ( . )    ',
    '   ┌───────────┐ ',
    '   │  ( •o• )  │)',
    '   │  |     |  │/',
    '   └───\\___/───┘ ',
  ],
  [
    '        ~  ( * ) ',
    '     ( ~ )  .    ',
    '   ┌───────────┐ ',
    '   │  ( •‿• )  │)',
    '   │  |     |  │/',
    '   └───\\___/───┘ ',
  ],
  [
    '     .  ( * )  ~ ',
    '       ( . )     ',
    '   ┌───────────┐ ',
    '   │  ( ^‿^ )  │)',
    '   │  |     |  │/',
    '   └───\\___/───┘ ',
  ],
];

const COFFEE_REST = [
  [
    '         z       ',
    '        Z   ( ~ )',
    '   ┌───────────┐ ',
    '   │  ( -.- )  │)',
    '   │  |  w  |  │/',
    '   └───\\___/───┘ ',
  ],
  [
    '        z        ',
    '       Z    ( · )',
    '   ┌───────────┐ ',
    '   │  ( >o< )  │)',
    '   │  |  O  |  │/',
    '   └───\\___/───┘ ',
  ],
];

const COFFEE_OVERTIME = [
  [
    '    * ( ✦ ) ~  * ',
    '     ( ~ ) ( * ) ',
    '   ┌───────────┐ ',
    '   │  ( O.O )  │)',
    '   │  |  !  |  │/',
    '   └───\\___/───┘ ',
  ],
  [
    '     ~ ( * ) ( ✦)',
    '    * ( ✦ ) ~    ',
    '   ┌───────────┐ ',
    '   │  ( O.O )  │)',
    '   │  |  !  |  │/',
    '   └───\\___/───┘ ',
  ],
];

// --- THEME 3: Coding Cat (from ascii-magic-art laptop-typing-cat & sleeping-cat) ---
const CAT_WORK = [
  [
    '       /\\_/\\   ┌───────┐',
    '      ( •.• )  │>_ code│',
    '      / > .    └───────┘',
    '     (______)===|=====| ',
    '     ~~~~~~~~~~~~~~~~~~ ',
  ],
  [
    '       /\\_/\\   ┌───────┐',
    '      ( •_• )  │>_ nap()',
    '      / . <    └───────┘',
    '     (______)===|=====| ',
    '     ~~~~~~~~~~~~~~~~~~ ',
  ],
  [
    '       /\\_/\\   ┌───────┐',
    '      ( ^.^ )  │>_ run │',
    '      / > .    └───────┘',
    '     (______)===|=====| ',
    '     ~~~~~~~~~~~~~~~~~~ ',
  ],
  [
    '       /\\_/\\   ┌───────┐',
    '      ( •o• )  │>_ ok! │',
    '      / . <    └───────┘',
    '     (______)===|=====| ',
    '     ~~~~~~~~~~~~~~~~~~ ',
  ],
];

const CAT_REST = [
  [
    '            z           ',
    '           Z            ',
    '       /\\_/\\            ',
    '      ( -.- )  ~*       ',
    '    (__________)        ',
  ],
  [
    '          z             ',
    '         Z              ',
    '       /\\_/\\            ',
    '      ( -.- )           ',
    '    (__________)        ',
  ],
];

const CAT_OVERTIME = [
  [
    '     ✦ /\\_/\\ ✦ ┌───────┐',
    '      ( >.< )  │>_ TURBO',
    '      / > >    └───────┘',
    '     (______)===|=====| ',
    '     ~~~~~~~~~~~~~~~~~~ ',
  ],
  [
    '     * /\\_/\\ * ┌───────┐',
    '      ( >o< )  │>_ FAST!',
    '      / < <    └───────┘',
    '     (______)===|=====| ',
    '     ~~~~~~~~~~~~~~~~~~ ',
  ],
];

// --- THEME 4: Debug Duck (from ascii-magic-art debug-duck-bob) ---
const DUCK_WORK = [
  [
    '       __     [ hmm.. ] ',
    '     <(o )___   /       ',
    '      ( ._> /           ',
    '     ~ ~ ~ ~ ~ ~ ~ ~ ~  ',
    '     ~~~~~~~~~~~~~~~~~  ',
  ],
  [
    '       __     [ line 42]',
    '     <(• )___   /       ',
    '      ( ._> /           ',
    '     ~ ~ ~ ~ ~ ~ ~ ~ ~  ',
    '     ~~~~~~~~~~~~~~~~~  ',
  ],
  [
    '       __     [ logic? ]',
    '     <(o )___   /       ',
    '      ( ._> /           ',
    '     ~ ~ ~ ~ ~ ~ ~ ~ ~  ',
    '     ~~~~~~~~~~~~~~~~~  ',
  ],
  [
    '       __     [ quack! ]',
    '     <(^ )___   /       ',
    '      ( ._> /           ',
    '     ~ ~ ~ ~ ~ ~ ~ ~ ~  ',
    '     ~~~~~~~~~~~~~~~~~  ',
  ],
];

const DUCK_REST = [
  [
    '       __        z      ',
    '     <(- )___   Z       ',
    '      ( ._> /           ',
    '     ~ ~ ~ ~ ~ ~ ~ ~ ~  ',
    '     ~~~~~~~~~~~~~~~~~  ',
  ],
  [
    '       __       z       ',
    '     <(- )___  Z        ',
    '      ( ._> /           ',
    '     ~ ~ ~ ~ ~ ~ ~ ~ ~  ',
    '     ~~~~~~~~~~~~~~~~~  ',
  ],
];

const DUCK_OVERTIME = [
  [
    '       __  ✦  [fixed! ✓]',
    '     <(^ )___   /       ',
    '      ( ._> /           ',
    '     ~ ~ ~ ~ ~ ~ ~ ~ ~  ',
    '     ~~~~~~~~~~~~~~~~~  ',
  ],
  [
    '       __  *  [DONE!  ✓]',
    '     <(^ )___   /       ',
    '      ( ._> /           ',
    '     ~ ~ ~ ~ ~ ~ ~ ~ ~  ',
    '     ~~~~~~~~~~~~~~~~~  ',
  ],
];

// --- THEME 5: Pixel Knight (from ascii-magic-art pixel-knight-salute) ---
const KNIGHT_WORK = [
  [
    '      ( )       ',
    '     /▓▓\\   |   ',
    '    [ •_•] -|==>',
    '    /|▓▓|\\  |   ',
    '   [▓|▓▓|▓]     ',
    '     ||||       ',
  ],
  [
    '      ( )   ^   ',
    '     /▓▓\\   |   ',
    '    [ •_•] /|   ',
    '    /|▓▓|\\/     ',
    '   [▓|▓▓|▓]     ',
    '     ||||       ',
  ],
  [
    '     *( )*  ✦   ',
    '     /▓▓\\   |   ',
    '    [ ^_^] /|   ',
    '    /|▓▓|\\/     ',
    '   [▓|▓▓|▓]     ',
    '     ||||       ',
  ],
  [
    '      ( )   ^   ',
    '     /▓▓\\   |   ',
    '    [ •_•] /|   ',
    '    /|▓▓|\\/     ',
    '   [▓|▓▓|▓]     ',
    '     ||||       ',
  ],
];

const KNIGHT_REST = [
  [
    '      ( )       ',
    '     /▓▓\\       ',
    '    [ -.-]      ',
    '    /|▓▓|\\  |   ',
    '   [▓|▓▓|▓] |===',
    '     ||||       ',
  ],
  [
    '      ( )   z   ',
    '     /▓▓\\  Z    ',
    '    [ -.-]      ',
    '    /|▓▓|\\  |   ',
    '   [▓|▓▓|▓] |===',
    '     ||||       ',
  ],
];

const KNIGHT_OVERTIME = [
  [
    '    ✦ ( ) ✦ ⚔   ',
    '     /▓▓\\   |   ',
    '    [ ^o^] /|==>',
    '    /|▓▓|\\/     ',
    '   [▓|▓▓|▓]     ',
    '     ||||       ',
  ],
  [
    '    * ( ) * ★   ',
    '     /▓▓\\   |   ',
    '    [ ^o^] /|==>',
    '    /|▓▓|\\/     ',
    '   [▓|▓▓|▓]     ',
    '     ||||       ',
  ],
];

// --- THEME 6: Candle Flame (from ascii-magic-art candle-flame) ---
const CANDLE_WORK = [
  [
    '     ( * )     ',
    '     ) ( )     ',
    '       |       ',
    '     ┌───┐     ',
    '     │ █ │     ',
    '    ┌┴───┴┐    ',
  ],
  [
    '    (  . )     ',
    '    ( ) )      ',
    '       |       ',
    '     ┌───┐     ',
    '     │.█ │     ',
    '    ┌┴───┴┐    ',
  ],
  [
    '     ( * )     ',
    '     (  ( )    ',
    '       |       ',
    '     ┌───┐     ',
    '     │:█ │     ',
    '    ┌┴───┴┐    ',
  ],
  [
    '     ( .  )    ',
    '      ) (      ',
    '       |       ',
    '     ┌───┐     ',
    '     │:█:│     ',
    '    ┌┴───┴┐    ',
  ],
];

const CANDLE_REST = [
  [
    '       .       ',
    '       ·       ',
    '       |       ',
    '     ┌───┐     ',
    '     │ █ │     ',
    '    ┌┴───┴┐    ',
  ],
  [
    '       *       ',
    '       ·       ',
    '       |       ',
    '     ┌───┐     ',
    '     │ █ │     ',
    '    ┌┴───┴┐    ',
  ],
];

const CANDLE_OVERTIME = [
  [
    '    * ( ✦ ) *  ',
    '    ( ) ( ) )  ',
    '       |       ',
    '     ┌───┐     ',
    '     │:█:│     ',
    '    ┌┴───┴┐    ',
  ],
  [
    '    ✦ ( * ) ✦  ',
    '    ) ( ) ( )  ',
    '       |       ',
    '     ┌───┐     ',
    '     │:█:│     ',
    '    ┌┴───┴┐    ',
  ],
];

// --- THEME 7: Matrix Digital Rain ---
const MATRIX_WORK = [
  [
    ' 0 1 0 1 0 1 0 1 0 1 ',
    ' 1 0 1 0 1 0 1 0 1 0 ',
    ' 0 1 0 1 0 1 0 1 0 1 ',
    ' 1 0 1 0 1 0 1 0 1 0 ',
  ],
  [
    ' 1 0 0 1 1 0 1 0 0 1 ',
    ' 0 1 1 0 0 1 0 1 1 0 ',
    ' 1 0 0 1 1 0 1 0 0 1 ',
    ' 0 1 1 0 0 1 0 1 1 0 ',
  ],
  [
    ' 0 1 1 0 1 0 0 1 1 0 ',
    ' 1 0 0 1 0 1 1 0 0 1 ',
    ' 0 1 1 0 1 0 0 1 1 0 ',
    ' 1 0 0 1 0 1 1 0 0 1 ',
  ],
];

const MATRIX_REST = [
  [
    ' . . · · . . · · . . ',
    ' · · . . · · . . · · ',
    ' . . · · . . · · . . ',
    ' · · . . · · . . · · ',
  ],
  [
    ' · · . . · · . . · · ',
    ' . . · · . . · · . . ',
    ' · · . . · · . . · · ',
    ' . . · · . . · · . . ',
  ],
];

// --- THEME 8: Cosmic Stars ---
const STARS_WORK = [
  [
    ' .  *     ·   .   *  ',
    '   ·   ✦    .   ·    ',
    ' *   .    ·     *    ',
    '   ✦    *   .    ✦   ',
  ],
  [
    ' *  ·     .   *   ·  ',
    '   .   *    ·   ✦    ',
    ' ✦   *    .     ·    ',
    '   ·    ✦   *    .   ',
  ],
  [
    ' ·  ✦     *   ·   .  ',
    '   *   ·    ✦   *    ',
    ' .   ·    *     .    ',
    '   *    .   ·    *   ',
  ],
];

const STARS_REST = [
  [
    ' ·  ·     .   ·   ·  ',
    '   .   ·    ·   .    ',
    ' ·   .    ·     ·    ',
    '   .    ·   .    .   ',
  ],
  [
    ' .  ·     ·   .   ·  ',
    '   ·   .    .   ·    ',
    ' .   ·    .     ·    ',
    '   ·    .   ·    .   ',
  ],
];

// --- THEME 9: Lunar Phases ---
const MOON_PHASES = ['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘'];
function renderMoonFrame(frameIdx, progressPct, phase) {
  let mIdx;
  if (phase === 'WORK') {
    mIdx = Math.min(MOON_PHASES.length - 1, Math.floor(progressPct * MOON_PHASES.length));
  } else if (phase === 'OVERTIME') {
    mIdx = 4; // Full moon glowing
  } else {
    mIdx = frameIdx % MOON_PHASES.length;
  }
  const m = MOON_PHASES[mIdx];
  return [
    '  .       ✦       ·  ',
    `    (   ${m}   )   *   `,
    '  *       ·       .  ',
  ];
}

// --- THEME 10: Analog Clock ---
const CLOCK_PHASES = ['🕛', '🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚'];
function renderClockFrame(frameIdx) {
  const c = CLOCK_PHASES[frameIdx % CLOCK_PHASES.length];
  return [
    '     ┌─────────┐     ',
    `    │    ${c}    │     `,
    '     └─────────┘     ',
  ];
}

// --- THEME 11: Arcane Mage ---
const MAGE_WORK = [
  [
    '     /\\         ',
    '    /  \\    ✦   ',
    '   /____\\  (o)  ',
    '   ( •_•) -/ |  ',
    '  _/(   )\\___|  ',
  ],
  [
    '     /\\     .   ',
    '    /  \\    *   ',
    '   /____\\  (O)  ',
    '   ( •_•) -/ |  ',
    '  _/(   )\\___|  ',
  ],
  [
    '     /\\    * ✦  ',
    '    /  \\   (◎)  ',
    '   /____\\  / |  ',
    '   ( ^_^) -  |  ',
    '  _/(   )\\___|  ',
  ],
  [
    '     /\\     ✦   ',
    '    /  \\   (o) *',
    '   /____\\  / |  ',
    '   ( •_•) -  |  ',
    '  _/(   )\\___|  ',
  ],
];

const MAGE_REST = [
  [
    '     /\\         ',
    '    /  \\   z    ',
    '   /____\\  Z    ',
    '   ( -.-)  |    ',
    '  _/(   )\\___|  ',
  ],
  [
    '     /\\    z    ',
    '    /  \\  Z     ',
    '   /____\\       ',
    '   ( -.-)  |    ',
    '  _/(   )\\___|  ',
  ],
];

// --- THEME 12: RPG Slime ---
const SLIME_WORK = [
  [
    '      . ✦ .    ',
    '     / o \\     ',
    '    ( o.o )    ',
    '   (_______)   ',
  ],
  [
    '       ✦       ',
    '     / - \\     ',
    '    ( -.- )    ',
    '   (_________) ',
  ],
  [
    '      . * .    ',
    '     / o \\     ',
    '    ( •.• )    ',
    '   (_______)   ',
  ],
  [
    '      . ✦ .    ',
    '     / ^ \\     ',
    '    ( ^.^ )    ',
    '   (_______)   ',
  ],
];

const SLIME_REST = [
  [
    '          z    ',
    '     / - \\  Z  ',
    '    ( -.- )    ',
    '   (_________) ',
  ],
  [
    '        z      ',
    '     / - \\ Z   ',
    '    ( -.- )    ',
    '   (_________) ',
  ],
];

// --- THEME 13: Hourglass ---
function renderHourglassChamber(progressPct, frameIdx, phase) {
  let pct;
  if (phase === 'BREAK') {
    pct = Math.max(0.0, Math.min(1.0, 1.0 - progressPct));
  } else if (phase === 'OVERTIME') {
    pct = 1.0;
  } else {
    pct = Math.max(0.0, Math.min(1.0, progressPct));
  }

  const remaining = Math.max(0, Math.min(8, Math.round(8 * (1.0 - pct))));
  const top1Count = Math.min(5, Math.max(0, remaining - 3));
  const top2Count = Math.min(3, remaining);

  const bottom = 8 - remaining;
  const bot1Count = Math.min(3, bottom);
  const bot2Count = Math.min(5, Math.max(0, bottom - 3));

  const fillCentered = (count, width, char = '✦') => {
    const pad = Math.floor((width - count) / 2);
    const extra = (width - count) % 2;
    return ' '.repeat(pad) + char.repeat(count) + ' '.repeat(pad + extra);
  };

  const t1 = fillCentered(top1Count, 5, '✦');
  const t2 = fillCentered(top2Count, 3, '✦');
  const b1 = fillCentered(bot1Count, 3, '✦');
  const b2 = fillCentered(bot2Count, 5, '✦');

  let particle;
  if (phase === 'OVERTIME') {
    particle = ['★', '✦', '✳', '✸'][frameIdx % 4];
  } else if (pct >= 1.0) {
    particle = ' ';
  } else {
    particle = [':', '·', '*', '✦'][frameIdx % 4];
  }

  return [
    ' ╔═══════╗ ',
    ` ║ ${t1} ║ `,
    ` ║ \\${t2}/ ║ `,
    ` ║   ${particle}   ║ `,
    ` ║ /${b1}\\ ║ `,
    ` ║ ${b2} ║ `,
    ' ╚═══════╝ ',
  ];
}

export function getNextTheme(current) {
  if (!THEMES.includes(current)) return THEMES[0];
  const idx = THEMES.indexOf(current);
  return THEMES[(idx + 1) % THEMES.length];
}

export function getThemeDisplayName(theme) {
  return THEME_NAMES[theme] || 'Bonfire';
}

export function getAnimationLines(theme, phase, frameIdx, progressPct = 0.0) {
  if (theme === 'bonfire') {
    if (phase === 'BREAK') return [BONFIRE_REST[frameIdx % BONFIRE_REST.length], '~ Resting at the Bonfire ~'];
    if (phase === 'OVERTIME') return [BONFIRE_WORK[frameIdx % BONFIRE_WORK.length], '~ Fire Blazes Brightly ~'];
    return [BONFIRE_WORK[frameIdx % BONFIRE_WORK.length], '~ The Fire Burns ~'];
  }

  if (theme === 'coffee') {
    if (phase === 'BREAK') return [COFFEE_REST[frameIdx % COFFEE_REST.length], '~ Savoring the Break ~'];
    if (phase === 'OVERTIME') return [COFFEE_OVERTIME[frameIdx % COFFEE_OVERTIME.length], '~ Extra Caffeine Fuel! ~'];
    return [COFFEE_WORK[frameIdx % COFFEE_WORK.length], '~ Fresh Coffee Steaming ~'];
  }

  if (theme === 'cat') {
    if (phase === 'BREAK') return [CAT_REST[frameIdx % CAT_REST.length], '~ Cat is sleeping on cushion ~'];
    if (phase === 'OVERTIME') return [CAT_OVERTIME[frameIdx % CAT_OVERTIME.length], '~ Cat typing at hyper-speed! ~'];
    return [CAT_WORK[frameIdx % CAT_WORK.length], '~ Cat is writing code ~'];
  }

  if (theme === 'duck') {
    if (phase === 'BREAK') return [DUCK_REST[frameIdx % DUCK_REST.length], '~ Duck floating peacefully ~'];
    if (phase === 'OVERTIME') return [DUCK_OVERTIME[frameIdx % DUCK_OVERTIME.length], '~ Bug Squashed! Quack! ~'];
    return [DUCK_WORK[frameIdx % DUCK_WORK.length], '~ Explaining bug to duck ~'];
  }

  if (theme === 'knight') {
    if (phase === 'BREAK') return [KNIGHT_REST[frameIdx % KNIGHT_REST.length], '~ Knight resting at camp ~'];
    if (phase === 'OVERTIME') return [KNIGHT_OVERTIME[frameIdx % KNIGHT_OVERTIME.length], '~ Knight triumphant! ~'];
    return [KNIGHT_WORK[frameIdx % KNIGHT_WORK.length], '~ Knight standing guard ~'];
  }

  if (theme === 'candle') {
    if (phase === 'BREAK') return [CANDLE_REST[frameIdx % CANDLE_REST.length], '~ Soft candle glow ~'];
    if (phase === 'OVERTIME') return [CANDLE_OVERTIME[frameIdx % CANDLE_OVERTIME.length], '~ Flame burning bright! ~'];
    return [CANDLE_WORK[frameIdx % CANDLE_WORK.length], '~ Burning the midnight oil ~'];
  }

  if (theme === 'matrix') {
    if (phase === 'BREAK') return [MATRIX_REST[frameIdx % MATRIX_REST.length], '~ System in Standby ~'];
    if (phase === 'OVERTIME') return [MATRIX_WORK[frameIdx % MATRIX_WORK.length], '~ Mainframe Overclocked! ~'];
    return [MATRIX_WORK[frameIdx % MATRIX_WORK.length], '~ Entering the Matrix ~'];
  }

  if (theme === 'stars') {
    if (phase === 'BREAK') return [STARS_REST[frameIdx % STARS_REST.length], '~ Serene Cosmic Drift ~'];
    if (phase === 'OVERTIME') return [STARS_WORK[frameIdx % STARS_WORK.length], '~ Supernova Focus! ~'];
    return [STARS_WORK[frameIdx % STARS_WORK.length], '~ Navigating the Cosmos ~'];
  }

  if (theme === 'moon') {
    const cap = phase === 'BREAK' ? '~ Moonlit Rest ~' : phase === 'OVERTIME' ? '~ Full Moon Brilliance ~' : '~ Waxing Focus ~';
    return [renderMoonFrame(frameIdx, progressPct, phase), cap];
  }

  if (theme === 'clock') {
    const cap = phase === 'BREAK' ? '~ Time to Rest ~' : phase === 'OVERTIME' ? '~ Bonus Focus Minutes ~' : '~ Ticking Steady ~';
    return [renderClockFrame(frameIdx), cap];
  }

  if (theme === 'mage') {
    if (phase === 'BREAK') return [MAGE_REST[frameIdx % MAGE_REST.length], '~ Meditating & Restoring Mana ~'];
    if (phase === 'OVERTIME') return [MAGE_WORK[frameIdx % MAGE_WORK.length], '~ Mana Overflowing! ~'];
    return [MAGE_WORK[frameIdx % MAGE_WORK.length], '~ Channeling Arcane Focus ~'];
  }

  if (theme === 'slime') {
    if (phase === 'BREAK') return [SLIME_REST[frameIdx % SLIME_REST.length], '~ Slime is taking a nap ~'];
    if (phase === 'OVERTIME') return [SLIME_WORK[frameIdx % SLIME_WORK.length], '~ Slime is supercharged! ~'];
    return [SLIME_WORK[frameIdx % SLIME_WORK.length], '~ Slime is cheering you on! ~'];
  }

  if (theme === 'hourglass') {
    const cap = phase === 'BREAK' ? '~ Turning the Hourglass ~' : phase === 'OVERTIME' ? '~ Hourglass Overflowing! ~' : '~ Sands of Time trickling ~';
    return [renderHourglassChamber(progressPct, frameIdx, phase), cap];
  }

  return [[], ''];
}
