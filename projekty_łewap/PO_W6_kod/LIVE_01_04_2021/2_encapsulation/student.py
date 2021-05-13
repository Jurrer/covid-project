class Student:

    def __init__(self, name, surname, age):
        self.__name = name
        self.__surname = surname
        self.__age = age

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname

    def get_age(self):
        return self.__age

    def __count_n_of_fields(self):
        return len(self.__dict__)

    def __str__(self):
        cls_name = self.__class__.__name__
        attrs = {k.split("__")[-1]: v for k, v in self.__dict__.items()}
        return f"({cls_name}): {attrs} | Num of fields: {self.__count_n_of_fields()}"
