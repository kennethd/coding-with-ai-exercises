#!/usr/bin/env python3
"""Fetch a random Chuck Norris joke from api.chucknorris.io and print it."""

import json
import sys
import urllib.error
import urllib.request

API_URL = "https://api.chucknorris.io/jokes/random"


def fetch_joke() -> str:
    request = urllib.request.Request(
        API_URL,
        headers={"Accept": "application/json", "User-Agent": "joke.py"},
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        data = json.load(response)
    return data["value"]


def ask_for_another() -> bool:
    """Ask until the user answers yes or no. EOF or Ctrl+C counts as no."""
    while True:
        try:
            answer = input("Want another joke? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return False
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please answer yes or no.")


def main() -> int:
    while True:
        try:
            print(fetch_joke())
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError) as exc:
            print(f"Failed to fetch joke: {exc}", file=sys.stderr)
            return 1
        if not ask_for_another():
            break
    return 0


if __name__ == "__main__":
    sys.exit(main())
