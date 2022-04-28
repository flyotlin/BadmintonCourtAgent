import unittest

from ..src.checker import Checker


class TestChecker(unittest.TestCase):
    def setUp(self) -> None:
        self.checker = Checker()
        self.checker.login()

    def test_check(self):
        pass

    def tearDown(self) -> None:
        self.checker.logout()
        self.checker.bye()
