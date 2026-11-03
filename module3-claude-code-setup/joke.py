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


def main() -> int:
    try:
        print(fetch_joke())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError) as exc:
        print(f"Failed to fetch joke: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
