import re
from typing import List

from src.logger import AyeLogger


NULL = "NULL"

"""
A simple recursive descent parser.

Public parse_xxx() method returns integer.
Value >= 0:
    It means the value-th term in the grammar below.
    e.g., parse_help() returns 1 means `HELP -> COMMAND NULL`
Value < 0:
    It means the args provided failed to follow the grammar defined.

Grammar:
    HELP -> NULL|COMMAND NULL
    SET_TOKEN -> NULL|"help" NULL
    CHECK_COURTS -> "help" NULL|DATE COURT NULL
    SNAP_COURT -> "help" NULL|"check" NULL|DATE COURT TIME NULL

    COMMAND -> "set_token"|"check_courts"|"snap_court"
    DATE -> regular expression
    COURT -> regular expression
    TIME -> regular expression
"""


class AyeParser:
    def __init__(self, args: List[str]):
        self.args = args

        self._logger = AyeLogger().get()
        self._index = -1
        self.next_token = ""
        self.scan_token()

    def scan_token(self):
        self._index += 1
        if self._index >= len(self.args):
            self.next_token = NULL
        else:
            self.next_token = self.args[self._index]

    def parse_help(self) -> int:
        if self.next_token == NULL:
            return 0
        command = self._parse_command()
        if command == "":
            return -1
        self.scan_token()
        return self._parse_null(1)

    def parse_set_token(self) -> int:
        if self.next_token == "help":
            self.scan_token()
            return self._parse_null(1)
        if self.next_token == NULL:
            return 0
        return -1

    def parse_check_courts(self) -> int:
        if self.next_token == "help":
            self.scan_token()
            return self._parse_null(0)
        date = self._parse_date()
        if date == "":
            return -1
        self.scan_token()

        court = self._parse_court()
        if court == -1:
            return -1
        self.scan_token()

        return self._parse_null(1)

    def parse_snap_court(self) -> int:
        if self.next_token == "help":
            self.scan_token()
            return self._parse_null(0)
        if self.next_token == "check":
            self.scan_token()
            return self._parse_null(1)
        date = self._parse_date()
        if date == "":
            return -1
        self.scan_token()

        court = self._parse_court()
        if court == -1:
            return -1
        self.scan_token()

        time = self._parse_time()
        if time == "":
            return -1
        self.scan_token()
        return self._parse_null(2)

    def _parse_null(self, ret: int) -> int:
        if self.next_token == NULL:
            return ret
        return -1

    def _parse_command(self) -> str:
        commands = ["set_token", "check_courts", "snap_court"]
        if self.next_token in commands:
            return self.next_token
        return ""

    def _parse_date(self) -> str:
        pattern = "^(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1])$"
        if not re.match(pattern, self.next_token):
            return ""
        return self.next_token

    def _parse_court(self) -> int:
        s = self.next_token
        if not s.isnumeric():
            return -1
        if int(s) <= 0 or int(s) > 6:
            return -1
        return int(s)

    def _parse_time(self) -> str:
        pattern = "^(0[6-9]|1[0-9]|2[0-1]):00$"
        if not re.match(pattern, self.next_token):
            return ""
        return self.next_token
