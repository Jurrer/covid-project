from enum import Enum, auto, unique


@unique
class HeroType(Enum):
    FILEMON = auto()
    KLAKIER = auto()
    GARFIELD = auto()


class UnknownHeroTypeException(Exception):
    pass


class Hero:

    def __init__(self, name, type):
        self.__name = name
        self.__type = type
        self.__position_x = 0

    def jump(self):
        if self.__type == HeroType.FILEMON:
            self.__position_x += 4
        elif self.__type == HeroType.KLAKIER:
            self.__position_x += 10
        elif self.__type == HeroType.GARFIELD:
            self.__position_x += 1
        else:
            raise UnknownHeroTypeException(self.__type)
