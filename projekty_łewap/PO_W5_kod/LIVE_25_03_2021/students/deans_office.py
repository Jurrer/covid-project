import sys

from students.student import Student


class DeansOffice:

    def __init__(self):
        self.students = dict()

    def add_student(self, stud: Student):
        self.students[stud.album_id] = stud

    def remove_student(self, stud_id):
        ids = self.students.keys()

        if stud_id in ids:
            self.students.pop(stud_id)
        else:
            print(f"Cannot remove student (not found) by id: {stud_id}.", file=sys.stderr)

    def update_status(self, stud_id, new_status):
        maybe_student = self.students.get(stud_id)

        if maybe_student:
            maybe_student.update_status(new_status)
        else:
            print(f"Cannot update student (not found) by id: {stud_id}.", file=sys.stderr)

    def display_students_ver_2(self):
        print("-------------")
        print("Students (dean's office)")

        for stud in self.students.values():
            print(stud)

    def display_students(self):
        print("-------------")
        print("Students (dean's office) -- FORMATTED")
        header = "| {:>8} | {:^10} | {:^10} | {:^3} |".format("album_id", "name", "surname", "age")
        n = len(header)
        line = "=" * n

        print(header)
        print(line)

        for stud in self.students.values():
            print("| {:8d} | {:>10} | {:>10} | {:>3} |".format(stud.album_id, stud.name, stud.surname, stud.age))
