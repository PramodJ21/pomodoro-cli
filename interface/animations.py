"""Fantasy-themed pixel / ASCII animations for Pomodoro timer."""

THEMES = ["bonfire", "mage", "slime", "hourglass", "none"]

THEME_NAMES = {
    "bonfire": "Bonfire",
    "mage": "Arcane Mage",
    "slime": "RPG Slime",
    "hourglass": "Mana Hourglass",
    "none": "Off",
}

# --- THEME 1: Bonfire (Dark Souls styled coiled sword & flickering flames) ---
BONFIRE_WORK = [
    [
        "    (  . )    ",
        "  (  ) )  )   ",
        " (  ) ) (  )  ",
        "   |====|     ",
        " _/_||_\\_\\_   ",
    ],
    [
        "  ( *  )      ",
        " ( ) (  )     ",
        "( ) ( )  )    ",
        "   |====|     ",
        " _/_||_\\_\\_   ",
    ],
    [
        "    (  . )    ",
        "  (  ( ) )    ",
        " ( ) (  ) )   ",
        "   |====|     ",
        " _/_||_\\_\\_   ",
    ],
    [
        "    (   * )   ",
        "   ) ( (  )   ",
        "  ( ) ) (  )  ",
        "   |====|     ",
        " _/_||_\\_\\_   ",
    ],
]

BONFIRE_REST = [
    [
        "     .   *    ",
        "    ( · )     ",
        "   (  .  )    ",
        "   |====|     ",
        " _/_||_\\_\\_   ",
    ],
    [
        "    *   .     ",
        "     ( · )    ",
        "    (  .  )   ",
        "   |====|     ",
        " _/_||_\\_\\_   ",
    ],
]

# --- THEME 2: Arcane Mage (Wizard channeling mana) ---
MAGE_WORK = [
    [
        "     /\\         ",
        "    /  \\    ✦   ",
        "   /____\\  (o)  ",
        "   ( •_•) -/ |  ",
        "  _/(   )\\___|  ",
    ],
    [
        "     /\\     .   ",
        "    /  \\    *   ",
        "   /____\\  (O)  ",
        "   ( •_•) -/ |  ",
        "  _/(   )\\___|  ",
    ],
    [
        "     /\\    * ✦  ",
        "    /  \\   (◎)  ",
        "   /____\\  / |  ",
        "   ( ^_^) -  |  ",
        "  _/(   )\\___|  ",
    ],
    [
        "     /\\     ✦   ",
        "    /  \\   (o) *",
        "   /____\\  / |  ",
        "   ( •_•) -  |  ",
        "  _/(   )\\___|  ",
    ],
]

MAGE_REST = [
    [
        "     /\\         ",
        "    /  \\   z    ",
        "   /____\\  Z    ",
        "   ( -.-)  |    ",
        "  _/(   )\\___|  ",
    ],
    [
        "     /\\    z    ",
        "    /  \\  Z     ",
        "   /____\\       ",
        "   ( -.-)  |    ",
        "  _/(   )\\___|  ",
    ],
]

# --- THEME 3: RPG Slime (Bouncing / breathing companion) ---
SLIME_WORK = [
    [
        "      . ✦ .    ",
        "     / o \\     ",
        "    ( o.o )    ",
        "   (_______)   ",
    ],
    [
        "       ✦       ",
        "     / - \\     ",
        "    ( -.- )    ",
        "  (_________)  ",
    ],
    [
        "      . * .    ",
        "     / o \\     ",
        "    ( •.• )    ",
        "   (_______)   ",
    ],
    [
        "      . ✦ .    ",
        "     / ^ \\     ",
        "    ( ^.^ )    ",
        "   (_______)   ",
    ],
]

SLIME_REST = [
    [
        "          z    ",
        "     / - \\  Z  ",
        "    ( -.- )    ",
        "  (_________)  ",
    ],
    [
        "        z      ",
        "     / - \\ Z   ",
        "    ( -.- )    ",
        "  (_________)  ",
    ],
]


def _render_hourglass_chamber(progress_pct: float, frame_idx: int, phase: str) -> list[str]:
    """Generates an hourglass where mana sands trickle down based on elapsed progress."""
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
        f" ║  \\{t2}/  ║ ",
        f" ║   {particle}   ║ ",
        f" ║  /{b1}\\  ║ ",
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
    progress_pct: float = 0.0
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
            caption = "~ Sands of Mana trickling ~"
        return lines, caption

    return [], ""
