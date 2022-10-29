import unittest

from src.handler.handler import AyeHandler
from tests.handler.telegram_fakes import MockTelegramMessage, StubTelegramUpdate


class TestAyeHandler(unittest.TestCase):
    def test_reply(self):
        # arrange
        command = "help"
        expected = f"阿椰不懂指令 {command}\n"
        handler = AyeHandler(
            command=command,
            engine=None
        )
        message = MockTelegramMessage()
        update = StubTelegramUpdate(message)

        # act
        handler.reply("help_error", update, replaced_vars={
            "command": command
        })

        # assert
        self.assertEqual(message.calledTimes(), 1)
        self.assertIn(expected, message.repliedTexts())

    def test_help_command(self):
        # arrange
        command = "main"
        _username = "admin"
        _id = 123
        expected = f"{_username} [{_id}]，歡迎使用羽球場預約小幫手v2.0 - 阿椰\n以下為阿椰支援的指令:\n\n/help [COMMAND]: 查看可用的指令\n/set_token: 設定token\n/check_courts: 查詢目前可預約場地\n/snap_court: 設定自動預約場地\n"
        handler = AyeHandler(
            command=command,
            engine=None
        )
        message = MockTelegramMessage()
        update = StubTelegramUpdate(message)

        # act
        handler.reply("help_main", update, replaced_vars={
            "command": command,
            "username": _username,
            "id": _id
        })

        # assert
        self.assertEqual(message.calledTimes(), 1)
        self.assertIn(expected, message.repliedTexts())
