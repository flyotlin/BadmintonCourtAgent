from enum import Enum


class SubCommand(Enum):
    CREATE = 1
    DELETE = 2
    CHECK = 3


class WorkerTypeEnum(Enum):
    REMIND = 0
    POLL = 1
    RESERVE = 2
