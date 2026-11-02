# pomodoro-cli 🍅

A beautiful, zero-dependency terminal Pomodoro timer with 19 animated ASCII companions (downloaded from [ascii.rest](https://ascii.rest)), overtime tracking, and rich productivity statistics.

Built entirely in modern **Node.js (ESM)** using Node's built-in `node:sqlite` engine.

---

## ✨ Features

- **⚡ Zero External Dependencies:** Powered completely by Node.js built-ins (`node:sqlite`, `node:readline`, ANSI terminal canvas). No `npm install` needed.
- **🎨 19 Animated ASCII Companions:** Real-time fluid mathematical & artistic terminal animations downloaded from `ascii.rest`:
  - 🍩 **Donut 3D** (Andy Sloane's iconic lit 3D rotating torus, after `donut.c`)
  - 🐱 **Sleeping Cat** (peaceful tabby sleeping & breathing on paws with drifting Zs)
  - 🔥 **Cozy Campfire** (flickering log fire with sparks and embers)
  - ☕ **Steaming Coffee** (hot coffee cup with curling steam plumes)
  - ⏳ **Hourglass** (flowing sand grains turning with cycle)
  - 🧊 **Wireframe Cube** (stippled 3D hidden-line rotating cube)
  - 👾 **Matrix Rain** (falling streams of matrix cyber glyphs)
  - ✨ **Warp Starfield** (hyperspace star streaks rushing outward)
  - ⚽ **Bouncing Balls** (kinetic rubber balls with squash and stretch physics)
  - 🕯️ **Candle Flame** (tall wavering candle in a dark room)
  - 🌕 **Moon Phases** (waxing and waning lunar cycle)
  - 🧬 **DNA Double Helix** (turning double helix with base pairs)
  - 💡 **Fireflies** (flashing swarm of fireflies over twilight grass)
  - 🌌 **Spiral Galaxy** (tilted spinning galaxy with differential star speeds)
  - 🦊 **Sleeping Fox** (woodland fox curled up snoozing and breathing)
  - 💥 **Doom Fire** (classic PSX Doom fire generator algorithm)
  - 🐍 **Slithering Snake** (smooth S-curve slithering snake)
  - 🦉 **Night Owl** (wise owl blinking on a branch)
  - ⛵ **Ocean Swell** (sailboat riding gentle undulating ocean swells)
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
- **📥 Easily Download More Animations:** Download any piece from the 200+ library at [ascii.rest](https://ascii.rest) using:
  ```bash
  npm run download-animation <piece-name>
  ```

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
