class HeroReaderWriter:

    def read_from_file(self, filename): pass

    def write_to_file(self, filename): pass


class Hero:

    def __init__(self, name):
        self.__name = name


class Klakier(Hero, HeroReaderWriter):

    def __init__(self, name, age):
        super().__init__(name)
        self.__age = age

    def read_from_file(self, filename):
        raise NotImplementedError

    def write_to_file(self, filename):
        with open(filename, "a") as f:
            f.write(self.__age)