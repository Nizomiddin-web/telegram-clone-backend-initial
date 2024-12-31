from enum import Enum
from random import choice


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return [(choice.value,choice.name) for choice in cls]

    @classmethod
    def values(cls):
        return [choice.value for choice in cls]

class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"