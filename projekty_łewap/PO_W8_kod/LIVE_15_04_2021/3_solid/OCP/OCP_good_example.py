class Hero:

    def __init__(self, name):
        self.__name = name
        self.__position_x = 0

    def get_position_x(self):
        return self.__position_x

    def _jump(self, jump_value):
        self.__position_x += jump_value


class Filemon(Hero):

    def __init__(self, name):
        super().__init__(name)

    def jump(self):
        super()._jump(4)


class Klakier(Hero):

    def jump(self):
        super()._jump(10)


class Garfield(Hero):
    def jump(self):
        super()._jump(1)
