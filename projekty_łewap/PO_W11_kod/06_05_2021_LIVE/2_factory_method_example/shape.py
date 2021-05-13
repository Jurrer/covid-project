from math import pi


class Shape:
    def count_area(self): pass


class Circle(Shape):
    def __init__(self):
        self.__radius = 3

    def count_area(self):
        return pi * self.__radius ** 2


class Square(Shape):
    def __init__(self):
        self.__a = 4
        self.__b = 5

    def count_area(self):
        return self.__a * self.__b


class ShapeCreator:
    def create_shape(self) -> Shape: pass


class CircleCreator(ShapeCreator):

    def create_shape(self) -> Shape:
        return Circle()


class SquareCreator(ShapeCreator):
    def create_shape(self) -> Shape:
        return Square()
