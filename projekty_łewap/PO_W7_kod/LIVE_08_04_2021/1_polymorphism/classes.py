class A:
    def __init__(self, name="Default name"):
        self._name = name

    def do_sth(self):
        print("I'm just...", self._name)


class B(A):
    def __init__(self, name):
        super().__init__(name)

    def do_sth(self):
        super().do_sth()
        print("Tell me more...", self._name)


class C(B):
    def __init__(self, name):
        super().__init__(name)

    def do_sth(self):
        super().do_sth()
        print("Sth more...", self._name)
