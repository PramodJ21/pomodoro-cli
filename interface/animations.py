"""ASCII and pixel animations for Pomodoro timer.
Includes inspirations from ascii-magic-art and prebuilt animations from the rich library.
"""

try:
    import rich.spinner
    _RICH_SPINNERS = rich.spinner.SPINNERS
except ImportError:
    _RICH_SPINNERS = {}

THEMES = [
    "bonfire",
    "coffee",
    "cat",
    "duck",
    "knight",
    "candle",
    "matrix",
    "stars",
    "moon",
    "clock",
    "mage",
    "slime",
    "hourglass",
    "none",
]

THEME_NAMES = {
    "bonfire": "Bonfire",
    "coffee": "Coffee Mug",
    "cat": "Coding Cat",
    "duck": "Debug Duck",
    "knight": "Pixel Knight",
    "candle": "Candle Flame",
    "matrix": "Matrix Rain",
    "stars": "Cosmic Stars",
    "moon": "Lunar Phases",
    "clock": "Analog Clock",
    "mage": "Arcane Mage",
    "slime": "RPG Slime",
    "hourglass": "Hourglass",
    "none": "Off",
}

# --- THEME 1: Bonfire (Dark Souls coiled sword & flame, inspired by campfire) ---
BONFIRE_WORK = [
    [
        r"    (  . )    ",
        r"  (  ) )  )   ",
        r" (  ) ) (  )  ",
        r"   |====|     ",
        r" _/_||_\_\_   ",
    ],
    [
        r"  ( *  )      ",
        r" ( ) (  )     ",
        r"( ) ( )  )    ",
        r"   |====|     ",
        r" _/_||_\_\_   ",
    ],
    [
        r"    (  . )    ",
        r"  (  ( ) )    ",
        r" ( ) (  ) )   ",
        r"   |====|     ",
        r" _/_||_\_\_   ",
    ],
    [
        r"    (   * )   ",
        r"   ) ( (  )   ",
        r"  ( ) ) (  )  ",
        r"   |====|     ",
        r" _/_||_\_\_   ",
    ],
]

BONFIRE_REST = [
    [
        r"     .   *    ",
        r"    ( · )     ",
        r"   (  .  )    ",
        r"   |====|     ",
        r" _/_||_\_\_   ",
    ],
    [
        r"    *   .     ",
        r"     ( · )    ",
        r"    (  .  )   ",
        r"   |====|     ",
        r" _/_||_\_\_   ",
    ],
]


# --- THEME 2: Coffee Mug (from ascii-magic-art coffee-steam & yawning-coffee-cup) ---
COFFEE_WORK = [
    [
        r"      ( ~ )  .   ",
        r"     .  ( * )    ",
        r"   ┌───────────┐ ",
        r"   │  ( •‿• )  │)",
        r"   │  |     |  │/",
        r"   └───\___/───┘ ",
    ],
    [
        r"     ( * )  ~    ",
        r"        ( . )    ",
        r"   ┌───────────┐ ",
        r"   │  ( •o• )  │)",
        r"   │  |     |  │/",
        r"   └───\___/───┘ ",
    ],
    [
        r"        ~  ( * ) ",
        r"     ( ~ )  .    ",
        r"   ┌───────────┐ ",
        r"   │  ( •‿• )  │)",
        r"   │  |     |  │/",
        r"   └───\___/───┘ ",
    ],
    [
        r"     .  ( * )  ~ ",
        r"       ( . )     ",
        r"   ┌───────────┐ ",
        r"   │  ( ^‿^ )  │)",
        r"   │  |     |  │/",
        r"   └───\___/───┘ ",
    ],
]

COFFEE_REST = [
    [
        r"         z       ",
        r"        Z   ( ~ )",
        r"   ┌───────────┐ ",
        r"   │  ( -.- )  │)",
        r"   │  |  w  |  │/",
        r"   └───\___/───┘ ",
    ],
    [
        r"        z        ",
        r"       Z    ( · )",
        r"   ┌───────────┐ ",
        r"   │  ( >o< )  │)",
        r"   │  |  O  |  │/",
        r"   └───\___/───┘ ",
    ],
]

COFFEE_OVERTIME = [
    [
        r"    * ( ✦ ) ~  * ",
        r"     ( ~ ) ( * ) ",
        r"   ┌───────────┐ ",
        r"   │  ( O.O )  │)",
        r"   │  |  !  |  │/",
        r"   └───\___/───┘ ",
    ],
    [
        r"     ~ ( * ) ( ✦)",
        r"    * ( ✦ ) ~    ",
        r"   ┌───────────┐ ",
        r"   │  ( O.O )  │)",
        r"   │  |  !  |  │/",
        r"   └───\___/───┘ ",
    ],
]


# --- THEME 3: Coding Cat (from ascii-magic-art laptop-typing-cat & sleeping-cat) ---
CAT_WORK = [
    [
        r"       /\_/\   ┌───────┐",
        r"      ( •.• )  │>_ code│",
        r"      / > .    └───────┘",
        r"     (______)===|=====| ",
        r"     ~~~~~~~~~~~~~~~~~~ ",
    ],
    [
        r"       /\_/\   ┌───────┐",
        r"      ( •_• )  │>_ nap()",
        r"      / . <    └───────┘",
        r"     (______)===|=====| ",
        r"     ~~~~~~~~~~~~~~~~~~ ",
    ],
    [
        r"       /\_/\   ┌───────┐",
        r"      ( ^.^ )  │>_ run │",
        r"      / > .    └───────┘",
        r"     (______)===|=====| ",
        r"     ~~~~~~~~~~~~~~~~~~ ",
    ],
    [
        r"       /\_/\   ┌───────┐",
        r"      ( •o• )  │>_ ok! │",
        r"      / . <    └───────┘",
        r"     (______)===|=====| ",
        r"     ~~~~~~~~~~~~~~~~~~ ",
    ],
]

CAT_REST = [
    [
        r"            z           ",
        r"           Z            ",
        r"       /\_/\            ",
        r"      ( -.- )  ~*       ",
        r"    (__________)        ",
    ],
    [
        r"          z             ",
        r"         Z              ",
        r"       /\_/\            ",
        r"      ( -.- )           ",
        r"    (__________)        ",
    ],
]

CAT_OVERTIME = [
    [
        r"     ✦ /\_/\ ✦ ┌───────┐",
        r"      ( >.< )  │>_ TURBO",
        r"      / > >    └───────┘",
        r"     (______)===|=====| ",
        r"     ~~~~~~~~~~~~~~~~~~ ",
    ],
    [
        r"     * /\_/\ * ┌───────┐",
        r"      ( >o< )  │>_ FAST!",
        r"      / < <    └───────┘",
        r"     (______)===|=====| ",
        r"     ~~~~~~~~~~~~~~~~~~ ",
    ],
]


# --- THEME 4: Debug Duck (from ascii-magic-art debug-duck-bob) ---
DUCK_WORK = [
    [
        r"       __     [ hmm.. ] ",
        r"     <(o )___   /       ",
        r"      ( ._> /           ",
        r"     ~ ~ ~ ~ ~ ~ ~ ~ ~  ",
        r"     ~~~~~~~~~~~~~~~~~  ",
    ],
    [
        r"       __     [ line 42]",
        r"     <(• )___   /       ",
        r"      ( ._> /           ",
        r"     ~ ~ ~ ~ ~ ~ ~ ~ ~  ",
        r"     ~~~~~~~~~~~~~~~~~  ",
    ],
    [
        r"       __     [ logic? ]",
        r"     <(o )___   /       ",
        r"      ( ._> /           ",
        r"     ~ ~ ~ ~ ~ ~ ~ ~ ~  ",
        r"     ~~~~~~~~~~~~~~~~~  ",
    ],
    [
        r"       __     [ quack! ]",
        r"     <(^ )___   /       ",
        r"      ( ._> /           ",
        r"     ~ ~ ~ ~ ~ ~ ~ ~ ~  ",
        r"     ~~~~~~~~~~~~~~~~~  ",
    ],
]

DUCK_REST = [
    [
        r"       __        z      ",
        r"     <(- )___   Z       ",
        r"      ( ._> /           ",
        r"     ~ ~ ~ ~ ~ ~ ~ ~ ~  ",
        r"     ~~~~~~~~~~~~~~~~~  ",
    ],
    [
        r"       __       z       ",
        r"     <(- )___  Z        ",
        r"      ( ._> /           ",
        r"     ~ ~ ~ ~ ~ ~ ~ ~ ~  ",
        r"     ~~~~~~~~~~~~~~~~~  ",
    ],
]

DUCK_OVERTIME = [
    [
        r"       __  ✦  [fixed! ✓]",
        r"     <(^ )___   /       ",
        r"      ( ._> /           ",
        r"     ~ ~ ~ ~ ~ ~ ~ ~ ~  ",
        r"     ~~~~~~~~~~~~~~~~~  ",
    ],
    [
        r"       __  *  [DONE!  ✓]",
        r"     <(^ )___   /       ",
        r"      ( ._> /           ",
        r"     ~ ~ ~ ~ ~ ~ ~ ~ ~  ",
        r"     ~~~~~~~~~~~~~~~~~  ",
    ],
]


# --- THEME 5: Pixel Knight (from ascii-magic-art pixel-knight-salute) ---
KNIGHT_WORK = [
    [
        r"      ( )       ",
        r"     /▓▓\   |   ",
        r"    [ •_•] -|==>",
        r"    /|▓▓|\  |   ",
        r"   [▓|▓▓|▓]     ",
        r"     ||||       ",
    ],
    [
        r"      ( )   ^   ",
        r"     /▓▓\   |   ",
        r"    [ •_•] /|   ",
        r"    /|▓▓|\/     ",
        r"   [▓|▓▓|▓]     ",
        r"     ||||       ",
    ],
    [
        r"     *( )*  ✦   ",
        r"     /▓▓\   |   ",
        r"    [ ^_^] /|   ",
        r"    /|▓▓|\/     ",
        r"   [▓|▓▓|▓]     ",
        r"     ||||       ",
    ],
    [
        r"      ( )   ^   ",
        r"     /▓▓\   |   ",
        r"    [ •_•] /|   ",
        r"    /|▓▓|\/     ",
        r"   [▓|▓▓|▓]     ",
        r"     ||||       ",
    ],
]

KNIGHT_REST = [
    [
        r"      ( )       ",
        r"     /▓▓\       ",
        r"    [ -.-]      ",
        r"    /|▓▓|\  |   ",
        r"   [▓|▓▓|▓] |===",
        r"     ||||       ",
    ],
    [
        r"      ( )   z   ",
        r"     /▓▓\  Z    ",
        r"    [ -.-]      ",
        r"    /|▓▓|\  |   ",
        r"   [▓|▓▓|▓] |===",
        r"     ||||       ",
    ],
]

KNIGHT_OVERTIME = [
    [
        r"    ✦ ( ) ✦ ⚔   ",
        r"     /▓▓\   |   ",
        r"    [ ^o^] /|==>",
        r"    /|▓▓|\/     ",
        r"   [▓|▓▓|▓]     ",
        r"     ||||       ",
    ],
    [
        r"    * ( ) * ★   ",
        r"     /▓▓\   |   ",
        r"    [ ^o^] /|==>",
        r"    /|▓▓|\/     ",
        r"   [▓|▓▓|▓]     ",
        r"     ||||       ",
    ],
]


# --- THEME 6: Candle Flame (from ascii-magic-art candle-flame) ---
CANDLE_WORK = [
    [
        r"     ( * )     ",
        r"     ) ( )     ",
        r"       |       ",
        r"     ┌───┐     ",
        r"     │ █ │     ",
        r"    ┌┴───┴┐    ",
    ],
    [
        r"    (  . )     ",
        r"    ( ) )      ",
        r"       |       ",
        r"     ┌───┐     ",
        r"     │.█ │     ",
        r"    ┌┴───┴┐    ",
    ],
    [
        r"     ( * )     ",
        r"     (  ( )    ",
        r"       |       ",
        r"     ┌───┐     ",
        r"     │:█ │     ",
        r"    ┌┴───┴┐    ",
    ],
    [
        r"     ( .  )    ",
        r"      ) (      ",
        r"       |       ",
        r"     ┌───┐     ",
        r"     │:█:│     ",
        r"    ┌┴───┴┐    ",
    ],
]

CANDLE_REST = [
    [
        r"       .       ",
        r"       ·       ",
        r"       |       ",
        r"     ┌───┐     ",
        r"     │ █ │     ",
        r"    ┌┴───┴┐    ",
    ],
    [
        r"       *       ",
        r"       ·       ",
        r"       |       ",
        r"     ┌───┐     ",
        r"     │ █ │     ",
        r"    ┌┴───┴┐    ",
    ],
]

CANDLE_OVERTIME = [
    [
        r"    * ( ✦ ) *  ",
        r"    ( ) ( ) )  ",
        r"       |       ",
        r"     ┌───┐     ",
        r"     │:█:│     ",
        r"    ┌┴───┴┐    ",
    ],
    [
        r"    ✦ ( * ) ✦  ",
        r"    ) ( ) ( )  ",
        r"       |       ",
        r"     ┌───┐     ",
        r"     │:█:│     ",
        r"    ┌┴───┴┐    ",
    ],
]


# --- THEME 7: Matrix Digital Rain ---
MATRIX_WORK = [
    [
        r" 0 1 0 1 0 1 0 1 0 1 ",
        r" 1 0 1 0 1 0 1 0 1 0 ",
        r" 0 1 0 1 0 1 0 1 0 1 ",
        r" 1 0 1 0 1 0 1 0 1 0 ",
    ],
    [
        r" 1 0 0 1 1 0 1 0 0 1 ",
        r" 0 1 1 0 0 1 0 1 1 0 ",
        r" 1 0 0 1 1 0 1 0 0 1 ",
        r" 0 1 1 0 0 1 0 1 1 0 ",
    ],
    [
        r" 0 1 1 0 1 0 0 1 1 0 ",
        r" 1 0 0 1 0 1 1 0 0 1 ",
        r" 0 1 1 0 1 0 0 1 1 0 ",
        r" 1 0 0 1 0 1 1 0 0 1 ",
    ],
]

MATRIX_REST = [
    [
        r" . . · · . . · · . . ",
        r" · · . . · · . . · · ",
        r" . . · · . . · · . . ",
        r" · · . . · · . . · · ",
    ],
    [
        r" · · . . · · . . · · ",
        r" . . · · . . · · . . ",
        r" · · . . · · . . · · ",
        r" . . · · . . · · . . ",
    ],
]


# --- THEME 8: Cosmic Stars ---
STARS_WORK = [
    [
        r" .  *     ·   .   *  ",
        r"   ·   ✦    .   ·    ",
        r" *   .    ·     *    ",
        r"   ✦    *   .    ✦   ",
    ],
    [
        r" *  ·     .   *   ·  ",
        r"   .   *    ·   ✦    ",
        r" ✦   *    .     ·    ",
        r"   ·    ✦   *    .   ",
    ],
    [
        r" ·  ✦     *   ·   .  ",
        r"   *   ·    ✦   *    ",
        r" .   ·    *     .    ",
        r"   *    .   ·    *   ",
    ],
]

STARS_REST = [
    [
        r" ·  ·     .   ·   ·  ",
        r"   .   ·    ·   .    ",
        r" ·   .    ·     ·    ",
        r"   .    ·   .    .   ",
    ],
    [
        r" .  ·     ·   .   ·  ",
        r"   ·   .    .   ·    ",
        r" .   ·    .     ·    ",
        r"   ·    .   ·    .   ",
    ],
]


# --- THEME 9: Lunar Phases (using rich.spinner moon) ---
def _render_moon_frame(frame_idx: int, progress_pct: float, phase: str) -> list[str]:
    frames = _RICH_SPINNERS.get("moon", {}).get("frames", ["🌑 ", "🌓 ", "🌕 ", "🌗 "])
    if phase == "WORK":
        # Progresses from New Moon (0%) to Full Moon (100%)
        m_idx = min(len(frames) - 1, int(progress_pct * len(frames)))
    elif phase == "OVERTIME":
        m_idx = 4 % len(frames)  # Full moon glowing
    else:
        m_idx = frame_idx % len(frames)
    m = frames[m_idx].strip()
    return [
        r"  .       ✦       ·  ",
        f"     (   {m}   )   *   ",
        r"  *       ·       .  ",
    ]


# --- THEME 10: Analog Clock (using rich.spinner clock) ---
def _render_clock_frame(frame_idx: int, phase: str) -> list[str]:
    frames = _RICH_SPINNERS.get("clock", {}).get("frames", ["🕛 ", "🕒 ", "🕕 ", "🕘 "])
    c = frames[frame_idx % len(frames)].strip()
    return [
        r"     ┌─────────┐     ",
        f"     │    {c}    │     ",
        r"     └─────────┘     ",
    ]


# --- THEME 11: Arcane Mage (Wizard channeling mana) ---
MAGE_WORK = [
    [
        r"     /\         ",
        r"    /  \    ✦   ",
        r"   /____\  (o)  ",
        r"   ( •_•) -/ |  ",
        r"  _/(   )\___|  ",
    ],
    [
        r"     /\     .   ",
        r"    /  \    *   ",
        r"   /____\  (O)  ",
        r"   ( •_•) -/ |  ",
        r"  _/(   )\___|  ",
    ],
    [
        r"     /\    * ✦  ",
        r"    /  \   (◎)  ",
        r"   /____\  / |  ",
        r"   ( ^_^) -  |  ",
        r"  _/(   )\___|  ",
    ],
    [
        r"     /\     ✦   ",
        r"    /  \   (o) *",
        r"   /____\  / |  ",
        r"   ( •_•) -  |  ",
        r"  _/(   )\___|  ",
    ],
]

MAGE_REST = [
    [
        r"     /\         ",
        r"    /  \   z    ",
        r"   /____\  Z    ",
        r"   ( -.-)  |    ",
        r"  _/(   )\___|  ",
    ],
    [
        r"     /\    z    ",
        r"    /  \  Z     ",
        r"   /____\       ",
        r"   ( -.-)  |    ",
        r"  _/(   )\___|  ",
    ],
]


# --- THEME 12: RPG Slime (from ascii-magic-art bouncing-slime) ---
SLIME_WORK = [
    [
        r"      . ✦ .    ",
        r"     / o \     ",
        r"    ( o.o )    ",
        r"   (_______)   ",
    ],
    [
        r"       ✦       ",
        r"     / - \     ",
        r"    ( -.- )    ",
        r"   (_________) ",
    ],
    [
        r"      . * .    ",
        r"     / o \     ",
        r"    ( •.• )    ",
        r"   (_______)   ",
    ],
    [
        r"      . ✦ .    ",
        r"     / ^ \     ",
        r"    ( ^.^ )    ",
        r"   (_______)   ",
    ],
]

SLIME_REST = [
    [
        r"          z    ",
        r"     / - \  Z  ",
        r"    ( -.- )    ",
        r"   (_________) ",
    ],
    [
        r"        z      ",
        r"     / - \ Z   ",
        r"    ( -.- )    ",
        r"   (_________) ",
    ],
]


# --- THEME 13: Hourglass (from ascii-magic-art hourglass) ---
def _render_hourglass_chamber(progress_pct: float, frame_idx: int, phase: str) -> list[str]:
    """Generates an hourglass where sand trickles down based on elapsed progress."""
    if phase == "BREAK":
        pct = max(0.0, min(1.0, 1.0 - progress_pct))
    elif phase == "OVERTIME":
        pct = 1.0
    else:
        pct = max(0.0, min(1.0, progress_pct))

    remaining = max(0, min(8, int(round(8 * (1.0 - pct)))))
    top1_count = min(5, max(0, remaining - 3))
    top2_count = min(3, remaining)

    bottom = 8 - remaining
    bot1_count = min(3, bottom)
    bot2_count = min(5, max(0, bottom - 3))

    def fill_centered(count: int, width: int, char: str = "✦") -> str:
        pad = (width - count) // 2
        extra = (width - count) % 2
        return " " * pad + char * count + " " * (pad + extra)

    t1 = fill_centered(top1_count, 5, "✦")
    t2 = fill_centered(top2_count, 3, "✦")
    b1 = fill_centered(bot1_count, 3, "✦")
    b2 = fill_centered(bot2_count, 5, "✦")

    if phase == "OVERTIME":
        particle = ["★", "✦", "✳", "✸"][frame_idx % 4]
    elif pct >= 1.0:
        particle = " "
    else:
        particle = [":", "·", "*", "✦"][frame_idx % 4]

    return [
        " ╔═══════╗ ",
        f" ║ {t1} ║ ",
        f" ║ \\{t2}/ ║ ",
        f" ║   {particle}   ║ ",
        f" ║ /{b1}\\ ║ ",
        f" ║ {b2} ║ ",
        " ╚═══════╝ ",
    ]


def get_next_theme(current: str) -> str:
    """Cycles through the available themes."""
    if current not in THEMES:
        return THEMES[0]
    idx = THEMES.index(current)
    return THEMES[(idx + 1) % len(THEMES)]


def get_theme_display_name(theme: str) -> str:
    """Returns human-readable name for a theme key."""
    return THEME_NAMES.get(theme, "Bonfire")


def get_animation_lines(
    theme: str,
    phase: str,
    frame_idx: int,
    progress_pct: float = 0.0,
) -> tuple[list[str], str]:
    """
    Returns (lines, caption) for the active theme, phase, and frame.
    Lines is empty if theme is 'none' or unknown.
    """
    if theme == "bonfire":
        if phase == "BREAK":
            frames = BONFIRE_REST
            caption = "~ Resting at the Bonfire ~"
        elif phase == "OVERTIME":
            frames = BONFIRE_WORK
            caption = "~ Fire Blazes Brightly ~"
        else:
            frames = BONFIRE_WORK
            caption = "~ The Fire Burns ~"
        return frames[frame_idx % len(frames)], caption

    elif theme == "coffee":
        if phase == "BREAK":
            frames = COFFEE_REST
            caption = "~ Savoring the Break ~"
        elif phase == "OVERTIME":
            frames = COFFEE_OVERTIME
            caption = "~ Extra Caffeine Fuel! ~"
        else:
            frames = COFFEE_WORK
            caption = "~ Fresh Coffee Steaming ~"
        return frames[frame_idx % len(frames)], caption

    elif theme == "cat":
        if phase == "BREAK":
            frames = CAT_REST
            caption = "~ Cat is sleeping on cushion ~"
        elif phase == "OVERTIME":
            frames = CAT_OVERTIME
            caption = "~ Cat typing at hyper-speed! ~"
        else:
            frames = CAT_WORK
            caption = "~ Cat is writing code ~"
        return frames[frame_idx % len(frames)], caption

    elif theme == "duck":
        if phase == "BREAK":
            frames = DUCK_REST
            caption = "~ Duck floating peacefully ~"
        elif phase == "OVERTIME":
            frames = DUCK_OVERTIME
            caption = "~ Bug Squashed! Quack! ~"
        else:
            frames = DUCK_WORK
            caption = "~ Explaining bug to duck ~"
        return frames[frame_idx % len(frames)], caption

    elif theme == "knight":
        if phase == "BREAK":
            frames = KNIGHT_REST
            caption = "~ Knight resting at camp ~"
        elif phase == "OVERTIME":
            frames = KNIGHT_OVERTIME
            caption = "~ Knight triumphant! ~"
        else:
            frames = KNIGHT_WORK
            caption = "~ Knight standing guard ~"
        return frames[frame_idx % len(frames)], caption

    elif theme == "candle":
        if phase == "BREAK":
            frames = CANDLE_REST
            caption = "~ Soft candle glow ~"
        elif phase == "OVERTIME":
            frames = CANDLE_OVERTIME
            caption = "~ Flame burning bright! ~"
        else:
            frames = CANDLE_WORK
            caption = "~ Burning the midnight oil ~"
        return frames[frame_idx % len(frames)], caption

    elif theme == "matrix":
        if phase == "BREAK":
            frames = MATRIX_REST
            caption = "~ System in Standby ~"
        elif phase == "OVERTIME":
            frames = MATRIX_WORK
            caption = "~ Mainframe Overclocked! ~"
        else:
            frames = MATRIX_WORK
            caption = "~ Entering the Matrix ~"
        return frames[frame_idx % len(frames)], caption

    elif theme == "stars":
        if phase == "BREAK":
            frames = STARS_REST
            caption = "~ Serene Cosmic Drift ~"
        elif phase == "OVERTIME":
            frames = STARS_WORK
            caption = "~ Supernova Focus! ~"
        else:
            frames = STARS_WORK
            caption = "~ Navigating the Cosmos ~"
        return frames[frame_idx % len(frames)], caption

    elif theme == "moon":
        lines = _render_moon_frame(frame_idx, progress_pct, phase)
        if phase == "BREAK":
            caption = "~ Moonlit Rest ~"
        elif phase == "OVERTIME":
            caption = "~ Full Moon Brilliance ~"
        else:
            caption = "~ Waxing Focus ~"
        return lines, caption

    elif theme == "clock":
        lines = _render_clock_frame(frame_idx, phase)
        if phase == "BREAK":
            caption = "~ Time to Rest ~"
        elif phase == "OVERTIME":
            caption = "~ Bonus Focus Minutes ~"
        else:
            caption = "~ Ticking Steady ~"
        return lines, caption

    elif theme == "mage":
        if phase == "BREAK":
            frames = MAGE_REST
            caption = "~ Meditating & Restoring Mana ~"
        elif phase == "OVERTIME":
            frames = MAGE_WORK
            caption = "~ Mana Overflowing! ~"
        else:
            frames = MAGE_WORK
            caption = "~ Channeling Arcane Focus ~"
        return frames[frame_idx % len(frames)], caption

    elif theme == "slime":
        if phase == "BREAK":
            frames = SLIME_REST
            caption = "~ Slime is taking a nap ~"
        elif phase == "OVERTIME":
            frames = SLIME_WORK
            caption = "~ Slime is supercharged! ~"
        else:
            frames = SLIME_WORK
            caption = "~ Slime is cheering you on! ~"
        return frames[frame_idx % len(frames)], caption

    elif theme == "hourglass":
        lines = _render_hourglass_chamber(progress_pct, frame_idx, phase)
        if phase == "BREAK":
            caption = "~ Turning the Hourglass ~"
        elif phase == "OVERTIME":
            caption = "~ Hourglass Overflowing! ~"
        else:
            caption = "~ Sands of Time trickling ~"
        return lines, caption

    return [], ""
