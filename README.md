# pomodoro-cli 🍅

A beautiful, zero-dependency terminal Pomodoro timer with 14 animated ASCII companions, overtime tracking, and rich productivity statistics.

Built entirely in modern **Node.js (ESM)** using Node's built-in `node:sqlite` engine.

---

## ✨ Features

- **⚡ Zero External Dependencies:** Powered completely by Node.js built-ins (`node:sqlite`, `node:readline`, ANSI terminal canvas). No `npm install` needed.
- **🎨 14 Animated ASCII Companions:** Real-time multi-frame animations that react to work, overtime, and break phases:
  - ☕ **Coffee Mug** (steaming mug)
  - 🐱 **Coding Cat** (typing away)
  - 🦆 **Debug Duck** (rubber duck companion)
  - ⚔️ **Pixel Knight** (idle stance)
  - 🕯️ **Candle Flame** (flickering candle)
  - 👾 **Matrix Rain** (falling cyber glyphs)
  - ✨ **Cosmic Stars** (twinkling starfield)
  - 🌕 **Lunar Phases** (orbiting moon phases)
  - 🕰️ **Analog Clock** (rotating clock hands)
  - 🧙 **Arcane Mage** (pulsing mystic aura)
  - 🟢 **RPG Slime** (squishy bounce)
  - ⏳ **Hourglass** (falling grains of sand)
  - 🔥 **Bonfire** (Dark Souls coiled sword & flame)
  - 🚫 **Off** (minimalist clock only)
- **⏱️ Smart Timer & Overtime Tracking:**
  - Big 5-row digital block clock with progress bar.
  - Automatically transitions to overtime when focus finishes so extra effort is never lost.
  - Interactive break prompt to start break immediately or save & exit.
  - System notifications (`notify-send` on Linux) and terminal bell on phase changes.
- **📊 4 Statistics & Analytics Views:**
  1. **Horizontal Bars:** Last 7 days with daily totals and 4-week rolling averages.
  2. **Column Histogram:** Last 7 days vertical bar chart with max scale.
  3. **Activity Heatmap & Streaks:** 4-week GitHub-style commit grid (`░▒▓█`) with current streak and best streak.
  4. **Lifetime Records & Rank:** Total sessions, total focus time, best single day, daily average, and productivity rank (Novice to Ascended Master).
- **💾 Persistent SQLite Storage:** Automatically stores sessions in `$XDG_DATA_HOME/pomodoro_cli/pomodoro_cli.db` (or `~/.local/share/pomodoro_cli/pomodoro_cli.db`).

---

## 🚀 Getting Started

### Prerequisites

- **Node.js v22.0.0+** (tested and verified on Node v26 with native SQLite)

### Installation

Clone the repository and link it globally:

```bash
git clone git@github.com:PramodJ21/pomodoro-cli.git
cd pomodoro-cli
npm link
```

Now you can run it from anywhere:

```bash
pomodoro
# or
pomodoro-cli
```

### Running Directly

```bash
./bin/cli.js
# or
npm start
```

---

## 🎮 Keybindings & Controls

### Home Menu
| Key | Action |
| --- | --- |
| `↑` / `k` | Move cursor up |
| `↓` / `j` | Move cursor down |
| `Enter` | Select menu option |
| `t` / `Tab` | Cycle animation theme |
| `Ctrl+C` | Exit application |

### Session Timer
| Key | Action |
| --- | --- |
| `t` | Cycle companion animation theme |
| `b` | Skip straight to break phase |
| `q` | Stop session or finish break early |
| `Enter` | Start break (during overtime prompt) |

### Statistics
| Key | Action |
| --- | --- |
| `←` / `→`, `h` / `l` | Switch between views |
| `Tab` | Next view |
| `1` – `4` | Jump directly to view 1 (Bars), 2 (Columns), 3 (Heatmap), 4 (Records) |
| `q` / `Esc` | Return to Home menu |

---

## 🧪 Testing

Run the built-in test suite (uses Node's native test runner):

```bash
npm test
```

---

## 📄 License

MIT © [PRAMOD SANDEEP JOSHI](https://github.com/PramodJ21)
