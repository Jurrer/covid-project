class Group:

    def __init__(self):
        self.people = []

    def add(self, human):
        self.people.append(human)

    def __str__(self):
        cls_name = self.__class__.__name__
        attrs = self.__dict__
        return f"({cls_name}): {attrs}"
