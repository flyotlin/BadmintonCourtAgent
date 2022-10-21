import unittest

from src.parser import AyeParser


class TestParser(unittest.TestCase):
    def test_parse_help(self):
        parser = AyeParser([])
        ret = parser.parse_help()
        self.assertEqual(ret, 0)

    def test_parse_help_individual(self):
        parser = AyeParser(["set_token"])
        ret = parser.parse_help()
        self.assertEqual(ret, 1)

    def test_parse_help_error(self):
        args = [
            ["set_token", "feww"],
            ["few"],
            ["set_token", "check_courts", "snap_court"]
        ]
        for i in args:
            parser = AyeParser(i)
            ret = parser.parse_help()
            self.assertEqual(ret, -1)

    def test_parse_set_token(self):
        parser = AyeParser([])
        ret = parser.parse_set_token()
        self.assertEqual(ret, 0)

    def test_parse_set_token_help(self):
        parser = AyeParser(["help"])
        ret = parser.parse_set_token()
        self.assertEqual(ret, 1)

    def test_parse_set_token_error(self):
        args = [
            ["help", "feww"],
            ["few"],
            ["wwer", "wagef", "pwi"]
        ]
        for i in args:
            parser = AyeParser(i)
            ret = parser.parse_set_token()
            self.assertEqual(ret, -1)

    def test_parse_check_courts(self):
        parser = AyeParser(["03-05", "6"])
        ret = parser.parse_check_courts()
        self.assertEqual(ret, 1)

    def test_parse_check_courts_help(self):
        parser = AyeParser(["help"])
        ret = parser.parse_check_courts()
        self.assertEqual(ret, 0)

    def test_parse_check_courts_error(self):
        args = [
            ["help", "feww"],
            ["few"],
            ["wwer", "wagef", "pwi"],
            ["03-05", "0"],
            ["03-05", "7"],
            ["3-05", "3"],
            ["03-5", "3"],
        ]
        for i in args:
            parser = AyeParser(i)
            ret = parser.parse_check_courts()
            self.assertEqual(ret, -1)

    def test_parse_snap_court(self):
        parser = AyeParser(["03-05", "6", "18:00"])
        ret = parser.parse_snap_court()
        self.assertEqual(ret, 2)

    def test_parse_snap_court_help(self):
        parser = AyeParser(["help"])
        ret = parser.parse_snap_court()
        self.assertEqual(ret, 0)

    def test_parse_snap_court_check(self):
        parser = AyeParser(["check"])
        ret = parser.parse_snap_court()
        self.assertEqual(ret, 1)

    def test_parse_snap_court_error(self):
        args = [
            ["help", "feww"],
            ["few"],
            ["wwer", "wagef", "pwi"],
            ["03-05", "0"],
            ["03-05", "7"],
            ["3-05", "3"],
            ["03-5", "3"],
        ]
        for i in args:
            parser = AyeParser(i)
            ret = parser.parse_snap_court()
            self.assertEqual(ret, -1)
