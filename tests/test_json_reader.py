import os
import unittest

from src.agent import BadmintonReserveAgent
from src.json_reader import MessageReader


class TestMessageReader(unittest.TestCase):
    def setUp(self) -> None:
        pwd = os.path.abspath(os.path.dirname(__file__))
        self.path = os.path.join(pwd, "../resource/test_messages.json")

        self.reader = MessageReader(self.path)

    def testGetWhenKeyExist(self):
        # arrange
        key = "help_main"
        expected = "help_main\nmessage"

        # act
        actual = self.reader.get(key)

        # assert
        self.assertEqual(expected, actual)

    def testGetWhenKeyNotExist(self):
        # arrange
        key = "not_exist_key"

        # act & assert
        with self.assertRaises(Exception):
            self.reader.get(key)
