class Student:

    def __init__(self, name, surname, age, album_id, status):
        self.name = name
        self.surname = surname
        self.age = age
        self.album_id = album_id
        self.status = status

    def update_status(self, new_status):
        self.status = new_status

    def __str__(self):
        cls_name = self.__class__.__name__
        attrs = self.__dict__
        return "[{}: {}]".format(cls_name, attrs)

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "album_id": self.album_id
        }
