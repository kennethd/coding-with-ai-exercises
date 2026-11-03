#!/usr/bin/env python3
"""Interactive Chuck Norris jokes from api.chucknorris.io (standard library only)."""

import functools
import json
import os
import random
import shutil
import sys
import textwrap
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://api.chucknorris.io/jokes"
FETCH_ERRORS = (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError)
MENU = "[Enter] next  [c] category  [s] search  [q] quit"

# ANSI color codes
JOKE = "1;32"  # bold green
PROMPT = "36"  # cyan
INFO = "33"  # yellow
ERROR = "31"  # red


# --- Output helpers -------------------------------------------------------


def _enable_windows_ansi(stream) -> bool:
    """Turn on ANSI escape handling for a Windows console stream."""
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11 if stream is sys.stdout else -12)
        mode = ctypes.c_uint32()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        enable_virtual_terminal_processing = 0x0004
        return bool(kernel32.SetConsoleMode(handle, mode.value | enable_virtual_terminal_processing))
    except (AttributeError, OSError):
        return False


@functools.cache
def _use_color(stream) -> bool:
    if os.environ.get("NO_COLOR") or not stream.isatty():
        return False
    return os.name != "nt" or _enable_windows_ansi(stream)


def style(text: str, code: str, stream=sys.stdout) -> str:
    return f"\033[{code}m{text}\033[0m" if _use_color(stream) else text


def wrap(text: str) -> str:
    width = min(80, shutil.get_terminal_size().columns)
    return textwrap.fill(text, width=width)


def info(message: str) -> None:
    print(style(wrap(message), INFO))


def error(message: str) -> None:
    print(style(message, ERROR, sys.stderr), file=sys.stderr)


def show_joke(joke: str) -> None:
    print()
    print(style(wrap(joke), JOKE))
    print()


def read_line(prompt: str) -> str | None:
    """Read a line of input. Returns None on EOF or Ctrl+C."""
    try:
        answer = input(style(prompt, PROMPT))
    except (EOFError, KeyboardInterrupt):
        print()
        return None
    return answer.strip()


# --- API -----------------------------------------------------------------


def get_json(path: str, params: dict | None = None):
    url = f"{API_BASE}/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": "joke.py"},
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.load(response)


def fetch_random(category: str | None = None) -> str:
    params = {"category": category} if category else None
    return get_json("random", params)["value"]


def fetch_categories() -> list[str]:
    return get_json("categories")


def search_jokes(query: str) -> list[str]:
    return [joke["value"] for joke in get_json("search", {"query": query})["result"]]


# --- Interactive session --------------------------------------------------


class Session:
    """Tracks where the next joke comes from: a search, a category, or anywhere."""

    def __init__(self) -> None:
        self.category: str | None = None
        self.query: str | None = None
        self.matches: list[str] = []  # search results not shown yet

    def describe(self) -> str:
        if self.query is not None:
            return f'search: "{self.query}", {len(self.matches)} left'
        if self.category:
            return f"category: {self.category}"
        return "random"

    def next_joke(self) -> str:
        if self.query is not None:
            if self.matches:
                return self.matches.pop()
            info(f'No more matches for "{self.query}". Back to {self._fallback()} jokes.')
            self.query = None
        return fetch_random(self.category)

    def _fallback(self) -> str:
        return f'"{self.category}"' if self.category else "random"


def choose_category(session: Session) -> bool:
    """Let the user pick a category. Returns True if a joke should be shown."""
    categories = fetch_categories()
    # A non-breaking space keeps each number next to its name when wrapping.
    options = ["0)\xa0any"] + [f"{i})\xa0{name}" for i, name in enumerate(categories, 1)]
    print(wrap("  ".join(options)).replace("\xa0", " "))
    while True:
        answer = read_line(f"Pick a category [0-{len(categories)}, Enter to cancel]: ")
        if not answer:
            return False
        if answer.isdigit() and 0 <= int(answer) <= len(categories):
            break
        error("Please enter one of the numbers shown.")
    number = int(answer)
    session.category = categories[number - 1] if number else None
    session.query = None
    session.matches = []
    return True


def start_search(session: Session) -> bool:
    """Search for jokes by keyword. Returns True if a joke should be shown."""
    while True:
        query = read_line("Search for (Enter to cancel): ")
        if not query:
            return False
        if 3 <= len(query) <= 120:
            break
        error("Search words must be 3-120 characters long.")
    results = search_jokes(query)
    if not results:
        info(f'No jokes found for "{query}".')
        return False
    random.shuffle(results)
    info(f'Found {len(results)} joke(s) for "{query}". Press Enter to see the next one.')
    session.query = query
    session.matches = results
    return True


def main() -> int:
    if not sys.stdin.isatty():
        # Piped input: read as UTF-8 and drop a leading byte order mark,
        # which PowerShell can add.
        sys.stdin.reconfigure(encoding="utf-8-sig")
    session = Session()
    try:
        show_joke(session.next_joke())
    except FETCH_ERRORS as exc:
        error(f"Failed to fetch joke: {exc}")
        return 1

    while True:
        choice = read_line(f"({session.describe()}) {MENU}: ")
        if choice is None or choice.lower() in ("q", "quit"):
            break
        choice = choice.lower()
        try:
            if choice == "":
                show = True
            elif choice == "c":
                show = choose_category(session)
            elif choice == "s":
                show = start_search(session)
            else:
                error(f"Unknown command {choice!r}. Use Enter, c, s or q.")
                show = False
            if show:
                show_joke(session.next_joke())
        except FETCH_ERRORS as exc:
            error(f"Request failed: {exc}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
