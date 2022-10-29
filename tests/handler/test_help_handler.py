from typing import List
import unittest

from src.handler.help import HelpHandler
from tests.handler.telegram_fakes import MockTelegramMessage, StubTelegramContext, StubTelegramUpdate


class TestHelpHandler(unittest.TestCase):
    def assert_help_command(self, args: List[str], _username: str, _id: int, expected: str):
        context = StubTelegramContext(args)
        message = MockTelegramMessage(_username, _id)
        update = StubTelegramUpdate(message)

        handler = HelpHandler(None)
        cmd = handler.help_command()

        # act
        cmd(update, context)

        # assert
        self.assertEqual(message.calledTimes(), 1)
        self.assertIn(expected, message.repliedTexts())

    def test_help_command_main(self):
        args = []
        _username = "admin"
        _id = 1234
        expected = f"{_username} [{_id}]，歡迎使用羽球場預約小幫手v2.0 - 阿椰\n以下為阿椰支援的指令:\n\n/help [COMMAND]: 查看可用的指令\n/set_token: 設定token\n/check_courts: 查詢目前可預約場地\n/snap_court: 設定自動預約場地\n"

        self.assert_help_command(args, _username, _id, expected)

    def test_help_command_individual(self):
        args = ["snap_court"]
        _username = "admin"
        _id = 1234
        expected = f"/snap_court DATE COURT TIME\n/snap_court check"

        self.assert_help_command(args, _username, _id, expected)

    def test_help_command_invalid(self):
        args = ["wrong_command"]
        _username = "admin"
        _id = 1234
        expected = "指令參數錯誤，/help查看正確用法"

        self.assert_help_command(args, _username, _id, expected)
