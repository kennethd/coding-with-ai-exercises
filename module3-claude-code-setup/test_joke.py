"""Tests for joke.py. Run with: python -m unittest test_joke -v

The API is faked, so these tests run offline and give the same results every time.
"""

import io
import json
import os
import unittest
import urllib.error
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

import joke

CATEGORIES = ["animal", "dev", "science"]


def fake_api(path, params=None):
    """Stand-in for joke.get_json that mimics api.chucknorris.io responses."""
    params = params or {}
    if path == "categories":
        return list(CATEGORIES)
    if path == "random":
        return {"value": f"random joke ({params.get('category', 'any')})"}
    if path == "search":
        query = params["query"]
        if query == "nothing":
            return {"total": 0, "result": []}
        return {"total": 2, "result": [{"value": f"{query} joke 1"}, {"value": f"{query} joke 2"}]}
    raise AssertionError(f"unexpected API path: {path}")


class JokeTestCase(unittest.TestCase):
    """Turns colors off and fixes the terminal width so output is predictable."""

    def setUp(self):
        patches = [
            mock.patch.object(joke, "_use_color", return_value=False),
            mock.patch.object(joke.shutil, "get_terminal_size", return_value=os.terminal_size((80, 24))),
        ]
        for patch in patches:
            patch.start()
            self.addCleanup(patch.stop)


class TestApi(JokeTestCase):
    def fake_response(self, payload):
        response = mock.MagicMock()
        response.__enter__.return_value = io.BytesIO(json.dumps(payload).encode())
        return response

    def test_get_json_builds_url_with_params(self):
        with mock.patch.object(joke.urllib.request, "urlopen", return_value=self.fake_response({"ok": 1})) as urlopen:
            result = joke.get_json("search", {"query": "two words"})
        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, "https://api.chucknorris.io/jokes/search?query=two+words")
        self.assertEqual(request.get_header("Accept"), "application/json")
        self.assertEqual(urlopen.call_args.kwargs["timeout"], 10)
        self.assertEqual(result, {"ok": 1})

    def test_get_json_without_params(self):
        with mock.patch.object(joke.urllib.request, "urlopen", return_value=self.fake_response([])) as urlopen:
            joke.get_json("categories")
        self.assertEqual(urlopen.call_args.args[0].full_url, "https://api.chucknorris.io/jokes/categories")

    def test_fetch_random_with_and_without_category(self):
        with mock.patch.object(joke, "get_json", side_effect=fake_api) as get_json:
            self.assertEqual(joke.fetch_random(), "random joke (any)")
            self.assertEqual(joke.fetch_random("dev"), "random joke (dev)")
        get_json.assert_any_call("random", None)
        get_json.assert_any_call("random", {"category": "dev"})

    def test_fetch_categories(self):
        with mock.patch.object(joke, "get_json", side_effect=fake_api):
            self.assertEqual(joke.fetch_categories(), CATEGORIES)

    def test_search_jokes_returns_joke_text(self):
        with mock.patch.object(joke, "get_json", side_effect=fake_api):
            self.assertEqual(joke.search_jokes("code"), ["code joke 1", "code joke 2"])
            self.assertEqual(joke.search_jokes("nothing"), [])


class TestSession(JokeTestCase):
    def test_describe(self):
        session = joke.Session()
        self.assertEqual(session.describe(), "random")
        session.category = "dev"
        self.assertEqual(session.describe(), "category: dev")
        session.query, session.matches = "code", ["a", "b"]
        self.assertEqual(session.describe(), 'search: "code", 2 left')

    def test_search_matches_run_out_then_fall_back_to_category(self):
        session = joke.Session()
        session.category = "dev"
        session.query, session.matches = "code", ["only match"]
        out = io.StringIO()
        with mock.patch.object(joke, "get_json", side_effect=fake_api), redirect_stdout(out):
            self.assertEqual(session.next_joke(), "only match")
            self.assertEqual(session.next_joke(), "random joke (dev)")
        self.assertIn('No more matches for "code". Back to "dev" jokes.', out.getvalue())
        self.assertIsNone(session.query)


class TestMain(JokeTestCase):
    def run_main(self, *answers, api=fake_api):
        """Run main() with the given typed answers. Input ends with EOF after the last one."""
        stdin = mock.Mock()
        stdin.isatty.return_value = True
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(joke, "get_json", side_effect=api), \
                mock.patch("builtins.input", side_effect=[*answers, EOFError()]) as fake_input, \
                mock.patch("sys.stdin", stdin), \
                mock.patch.object(joke.random, "shuffle"), \
                redirect_stdout(out), redirect_stderr(err):
            code = joke.main()
        prompts = [call.args[0] for call in fake_input.call_args_list]
        return code, out.getvalue(), err.getvalue(), prompts

    def test_shows_joke_and_quits(self):
        code, out, _, prompts = self.run_main("q")
        self.assertEqual(code, 0)
        self.assertIn("random joke (any)", out)
        self.assertEqual(prompts, ["(random) [Enter] next  [c] category  [s] search  [q] quit: "])

    def test_quit_word_and_eof_both_exit(self):
        self.assertEqual(self.run_main("QUIT")[0], 0)
        self.assertEqual(self.run_main()[0], 0)  # EOF straight away

    def test_enter_fetches_another_joke(self):
        _, out, _, _ = self.run_main("", "", "q")
        self.assertEqual(out.count("random joke (any)"), 3)

    def test_unknown_command(self):
        _, _, err, _ = self.run_main("x", "q")
        self.assertIn("Unknown command 'x'. Use Enter, c, s or q.", err)

    def test_first_fetch_failure_exits_with_1(self):
        def broken(path, params=None):
            raise urllib.error.URLError("no network")

        code, _, err, prompts = self.run_main("q", api=broken)
        self.assertEqual(code, 1)
        self.assertIn("Failed to fetch joke", err)
        self.assertEqual(prompts, [])

    def test_later_failure_keeps_menu_running(self):
        calls = []

        def flaky(path, params=None):
            calls.append(path)
            if len(calls) == 2:
                raise urllib.error.URLError("blip")
            return fake_api(path, params)

        code, out, err, _ = self.run_main("", "", "q", api=flaky)
        self.assertEqual(code, 0)
        self.assertIn("Request failed", err)
        self.assertEqual(out.count("random joke (any)"), 2)

    def test_pick_category_after_invalid_choices(self):
        code, out, err, prompts = self.run_main("c", "9", "abc", "2", "", "q")
        self.assertEqual(code, 0)
        self.assertIn("0) any  1) animal  2) dev  3) science", out)
        self.assertEqual(err.count("Please enter one of the numbers shown."), 2)
        self.assertEqual(out.count("random joke (dev)"), 2)
        self.assertTrue(prompts[-1].startswith("(category: dev)"))

    def test_category_zero_goes_back_to_any(self):
        _, out, _, prompts = self.run_main("c", "2", "c", "0", "q")
        self.assertEqual(out.count("random joke (any)"), 2)
        self.assertTrue(prompts[-1].startswith("(random)"))

    def test_category_cancel(self):
        _, out, _, prompts = self.run_main("c", "", "q")
        self.assertEqual(out.count("random joke"), 1)
        self.assertTrue(prompts[-1].startswith("(random)"))

    def test_search_walks_matches_then_falls_back(self):
        _, out, err, prompts = self.run_main("s", "ab", "code", "", "", "q")
        self.assertIn("Search words must be 3-120 characters long.", err)
        self.assertIn('Found 2 joke(s) for "code".', out)
        # Matches are shown from the end of the (unshuffled) list.
        self.assertLess(out.index("code joke 2"), out.index("code joke 1"))
        self.assertIn('No more matches for "code". Back to random jokes.', out)
        self.assertIn('(search: "code", 1 left)', prompts[-3])
        self.assertTrue(prompts[-1].startswith("(random)"))

    def test_search_with_no_results(self):
        _, out, _, prompts = self.run_main("s", "nothing", "q")
        self.assertIn('No jokes found for "nothing".', out)
        self.assertEqual(out.count("random joke"), 1)
        self.assertTrue(prompts[-1].startswith("(random)"))

    def test_search_cancel(self):
        _, out, _, _ = self.run_main("s", "", "q")
        self.assertEqual(out.count("random joke"), 1)

    def test_piped_input_with_byte_order_mark(self):
        # Simulates PowerShell piping "q" with a BOM to Python on Windows (cp1252 default).
        stdin = io.TextIOWrapper(io.BytesIO(b"\xef\xbb\xbfq\n"), encoding="cp1252")
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(joke, "get_json", side_effect=fake_api), \
                mock.patch("sys.stdin", stdin), redirect_stdout(out), redirect_stderr(err):
            code = joke.main()
        self.assertEqual(code, 0)
        self.assertEqual(err.getvalue(), "")


class TestOutput(JokeTestCase):
    def test_wrap_respects_terminal_width(self):
        text = "word " * 50
        self.assertTrue(all(len(line) <= 80 for line in joke.wrap(text).splitlines()))
        with mock.patch.object(joke.shutil, "get_terminal_size", return_value=os.terminal_size((30, 24))):
            self.assertTrue(all(len(line) <= 30 for line in joke.wrap(text).splitlines()))

    def test_category_list_keeps_numbers_with_names(self):
        out = io.StringIO()
        with mock.patch.object(joke, "get_json", side_effect=fake_api), \
                mock.patch.object(joke.shutil, "get_terminal_size", return_value=os.terminal_size((20, 24))), \
                mock.patch("builtins.input", return_value=""), redirect_stdout(out):
            joke.choose_category(joke.Session())
        for line in out.getvalue().splitlines():
            self.assertFalse(line.endswith(")"), f"number split from its name: {line!r}")
        self.assertNotIn("\xa0", out.getvalue())

    def test_style_with_and_without_color(self):
        self.assertEqual(joke.style("hi", joke.ERROR), "hi")
        with mock.patch.object(joke, "_use_color", return_value=True):
            self.assertEqual(joke.style("hi", joke.ERROR), "\033[31mhi\033[0m")


class TestUseColor(unittest.TestCase):
    """Tests the real _use_color (not patched), clearing its cache around each test."""

    def setUp(self):
        joke._use_color.cache_clear()
        self.addCleanup(joke._use_color.cache_clear)
        self.tty = mock.Mock()
        self.tty.isatty.return_value = True

    def test_off_when_not_a_terminal(self):
        pipe = mock.Mock()
        pipe.isatty.return_value = False
        self.assertFalse(joke._use_color(pipe))

    def test_off_when_no_color_is_set(self):
        with mock.patch.dict(os.environ, {"NO_COLOR": "1"}):
            self.assertFalse(joke._use_color(self.tty))

    def test_on_for_linux_terminal_without_windows_calls(self):
        with mock.patch.dict(os.environ, clear=True), \
                mock.patch.object(joke.os, "name", "posix"), \
                mock.patch.object(joke, "_enable_windows_ansi") as enable_windows:
            self.assertTrue(joke._use_color(self.tty))
        enable_windows.assert_not_called()

    def test_windows_depends_on_console_setup(self):
        for enabled in (True, False):
            joke._use_color.cache_clear()
            with mock.patch.dict(os.environ, clear=True), \
                    mock.patch.object(joke.os, "name", "nt"), \
                    mock.patch.object(joke, "_enable_windows_ansi", return_value=enabled):
                self.assertEqual(joke._use_color(self.tty), enabled)


if __name__ == "__main__":
    unittest.main()
