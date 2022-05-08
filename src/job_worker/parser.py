import re

from datetime import time
from typing import List, TypedDict

from src.exceptions import JobWorkerParseError
from src.enums import SubCommand


class JobWorkerParser:
    def __init__(self) -> None:
        self._args: TypedDict('args', {
            'days': str,
            'times': str,
            'id': int
        }) = {
            'days': None,
            'times': None,
            'id': None
        }

    def parse(self, _args: List[str]) -> SubCommand:
        if len(_args) <= 0 or len(_args) >= 3:
            raise JobWorkerParseError("check 後面不能接這些 args，請參考 /help check")
        if len(_args) == 1:
            if _args[0] == 'check':
                return SubCommand.CHECK
            else:
                raise JobWorkerParseError("沒有此指令，請參考 /help check")
        if len(_args) == 2:
            if _args[0] == 'delete':
                if not _args[1].isnumeric():
                    raise JobWorkerParseError("delete id 要是數字椰，請參考 /help check")
                self._args['id'] = int(_args[1])
                return SubCommand.DELETE
            else:
                if not re.match("^[0-6](,[0-6])*$", _args[0]):
                    raise JobWorkerParseError("星期格式錯誤，請參考 /help check")
                # times
                if not re.match("^(([0-1][0-9]|2[0-3])\:([0-5][0-9]))(\,([0-1][0-9]|2[0-3])\:([0-5][0-9]))*$", _args[1]):
                    print('wrong times')
                    raise JobWorkerParseError("時間格式錯誤，請參考 /help check")
                self._args['days'] = _args[0]
                self._args['times'] = _args[1]
                return SubCommand.CREATE

    def get_days(self):
        days = self._args['days']
        days = tuple(map(int, days.split(',')))
        return days

    def get_times(self):
        times = self._args['times']
        times = tuple(map(lambda x: time(hour=int(x.split(':')[0]), minute=int(x.split(':')[1])), times.split(',')))
        return times

    def get_delete_id(self):
        return self._args['id']
