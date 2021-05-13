from enum import Enum, auto, unique


@unique
class NumGeneratorType(Enum):
    RANDOM = auto()
    ASCENDING = auto()
    DESCENDING = auto()
