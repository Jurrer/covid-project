class Name:
    def __init__(self, name):
        self.name = name

    def __add__(self, other):
        return f"{self.name}_{other.name}"

    def __str__(self):
        cls_name = self.__class__.__name__
        attrs = self.__dict__
        return "[{}: {}]".format(cls_name, attrs)
