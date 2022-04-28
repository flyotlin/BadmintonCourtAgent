import unittest

from ..src.agent import Agent


class TestAgent(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = Agent()
        self.agent.login()

    def test_login(self):
        pass

    def test_logout(self):
        pass

    def tearDown(self) -> None:
        self.agent.logout()
        self.agent.bye()
