class Student:
    def __init__(self, name, surname, birthdate):
        self.__name = name
        self.__surname = surname
        self.__birthdate = birthdate

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname

    def get_birthdate(self):
        return self.__birthdate

    def __repr__(self):
        cls = self.__class__.__name__
        attrs = {k.split("__")[-1]: v for k, v in self.__dict__.items()}
        return f"[{cls}: {attrs}]"

    def __hash__(self):
        print("Jestem w hash")
        return (self.__name, self.__surname, self.__birthdate).__hash__()

    def __eq__(self, other):
        print("Jestem w eq")
        return self.__class__ == other.__class__ \
               and self.__name == other.get_name() \
               and self.__surname == other.get_surname() \
               and self.__birthdate == other.get_birthdate()
