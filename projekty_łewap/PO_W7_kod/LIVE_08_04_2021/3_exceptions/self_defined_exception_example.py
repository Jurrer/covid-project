class StudentNotFoundException(Exception):
    def __init__(self, message):
        super().__init__("Sth more: " + message)


class A:
    def do_sth(self):
        raise StudentNotFoundException("Cannot find student by name: %s" % "Filemon")


a = A()
try:
    a.do_sth()
except StudentNotFoundException as e:
    print(e)
