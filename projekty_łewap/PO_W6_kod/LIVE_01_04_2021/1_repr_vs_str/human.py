class Human:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    def __str__(self):
        cls_name = self.__class__.__name__
        attrs = self.__dict__
        return f"({cls_name}): {attrs}"

    def __repr__(self):
        cls_name = self.__class__.__name__
        attrs = self.__dict__
        return f"[{cls_name}]: {attrs}"
