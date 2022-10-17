import json
import os


class JsonReader:
    def __init__(self, path: str) -> None:
        self.path = path

    def read(self) -> dict:
        with open(self.path, "r") as f:
            json_str = f.read()
            return json.loads(json_str)


class MessageReader(JsonReader):
    def __init__(self, path=None) -> None:
        if path is None:
            pwd = os.path.abspath(os.path.dirname(__file__))
            path = os.path.join(pwd, "../resource/messages.json")

        super().__init__(path)

    def get(self, key: str, **kwargs) -> str:
        """Get message from `messages.json` with key.

        You can provide additional kwargs to replace variables {{}} in message.
        """
        messages = self.read()
        if key not in messages.keys():
            raise Exception(f"failed to find key [{key}] in messages.json")

        messages = messages[key]["message"]
        for k, v in kwargs.items():
            messages = self._replace_variables(messages, k, v)

        return messages

    def _replace_variables(self, msg: str, key: str, value: str) -> None:
        key, value = str(key), str(value)
        return msg.replace(f"{{{{{key}}}}}", value)  # 1 {{}} can escape {}
