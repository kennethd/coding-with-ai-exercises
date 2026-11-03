# Plan: make joke.py more interactive (categories, search, colors + wrap)

## Context
`module3-claude-code-setup/joke.py` currently prints a random Chuck Norris joke and asks
"Want another joke? (y/n)". The user picked three upgrades: a command menu with
category selection, keyword search, and colored + word-wrapped output.
Constraint: standard library only (no 3rd-party packages).

API endpoints used (api.chucknorris.io):
- `GET /jokes/random` and `GET /jokes/random?category=<name>` -> `{"value": ...}`
- `GET /jokes/categories` -> `["animal", "career", "dev", ...]`
- `GET /jokes/search?query=<text>` -> `{"total": N, "result": [{"value": ...}, ...]}` (query must be 3-120 chars)

## Changes (single file: `module3-claude-code-setup/joke.py`)

### 1. HTTP helper
- Replace `fetch_joke()` with `get_json(path, params=None)` that builds the URL with
  `urllib.parse.urlencode`, keeps the existing headers/timeout, and returns parsed JSON.
- Thin wrappers: `fetch_random(category=None)`, `fetch_categories()`, `search_jokes(query)`.

### 2. Command menu (replaces `ask_for_another`)
After each joke, show:
`[Enter] next  [c] category  [s] search  [q] quit` plus the current mode, e.g. `(category: dev)` or `(search: "code", 3 left)`.
- **Enter**: next joke from the current mode (random, random-in-category, or next search match).
- **c**: fetch categories, show a numbered list with `0 = any`; invalid input re-prompts. Sets mode, then shows a joke.
- **s**: prompt for a search word (re-prompt if < 3 chars). Show "Found N jokes", shuffle results, show the first.
  Enter walks through the remaining matches; when they run out, say so and fall back to random mode.
  Zero matches -> message, stay in the previous mode.
- **q**, EOF, or Ctrl+C: quit. Unknown keys -> short help line.
- Strip a leading BOM (`﻿`) from input, fixing the earlier PowerShell-pipe issue.
- `main()` keeps the loop with `break` on quit and `return 0` as its last line (user's preferred style).
- Network/JSON errors now print an error and return to the menu instead of exiting,
  so one failed request doesn't end the session. (Exit 1 only if the very first fetch fails.)

### 3. Colors + word wrap
- Small `style(text, code)` helper using ANSI codes: joke in bold/bright, prompts/menu in cyan,
  info ("Found N jokes") in yellow, errors in red (to stderr).
- Colors on only when `sys.stdout.isatty()` and `NO_COLOR` is not set.
  On Windows, enable ANSI via `ctypes` `SetConsoleMode(... | ENABLE_VIRTUAL_TERMINAL_PROCESSING)`, wrapped in try/except (falls back to no color).
- Wrap jokes with `textwrap.fill(width=min(80, shutil.get_terminal_size().columns))`.

## Verification
From Bash in `module3-claude-code-setup/` (piped output = no colors, which also tests that path):
1. `printf '\n\nq\n' | python joke.py` -> 3 random jokes, exit 0.
2. `printf 'c\n<n for dev>\n\nq\n' | python joke.py` -> category list, then dev jokes.
3. `printf 's\nab\ncomputer\n\n\nq\n' | python joke.py` -> rejects "ab", shows match count, walks matches.
4. `printf 's\nzzqqxx\nq\n' | python joke.py` -> "no matches" message, menu continues.
5. `printf 'x\nq\n' | python joke.py` -> help line for unknown key.
6. User runs `python joke.py` in their terminal to see colors and wrapping; `NO_COLOR=1` disables colors.
