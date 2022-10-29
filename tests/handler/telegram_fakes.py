from typing import List


class StubTelegramUpdate:
    def __init__(self, message) -> None:
        self.message = message


class MockTelegramMessage:
    def __init__(self, username="", user_id=0) -> None:
        self._called_times = 0
        self._recorded_reply_texts = []

        self.from_user = StubTelegramFromUser(username, user_id)

    def reply_text(self, msg, **kwargs):
        self._called_times += 1
        self._recorded_reply_texts.append(msg)

    def calledTimes(self) -> int:
        times = self._called_times

        # reset
        self._called_times = 0
        return times

    def repliedTexts(self) -> List[str]:
        texts = self._recorded_reply_texts.copy()

        # reset
        self._recorded_reply_texts.clear()
        return texts


class StubTelegramContext:
    def __init__(self, args: List[str]):
        self.args = args


class StubTelegramFromUser:
    def __init__(self, username, user_id):
        self.username = username
        self.id = user_id
