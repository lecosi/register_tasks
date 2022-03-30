from enum import Enum


class PriorityTask(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class TaskStatusConstant(Enum):
    CREATED = 1
    IN_PROCESS = 2
    DONE = 3
