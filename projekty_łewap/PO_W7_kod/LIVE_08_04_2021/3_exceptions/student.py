from exceptions_classes import InvalidStudentParamsException


class Student:
    def __init__(self, name):
        self.__validate_args(name)
        self.__name = name

    def __validate_args(self, name):
        if not isinstance(name, str) or len(name) < 1:
            raise InvalidStudentParamsException("name")
