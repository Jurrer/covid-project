class StudentView:
    def print_all_info(self, students): pass

    def print_only_names(self, students): pass


class StudentViewWithSpace(StudentView):

    def print_all_info(self, students):
        for student in students:
            print("%s\t\t%s\t\t%s".format(student.get_name(), student.get_surname(), student.get_age()))

    def print_only_names(self, students):
        for student in students:
            print(student.get_name())


class StudentViewShortInfo(StudentView):

    def print_all_info(self, students):
        for student in students:
            print("%s %s %s".format(student.get_name(), student.get_surname(), student.get_age()))

    def print_only_names(self, students):
        raise NotImplementedError("Not implemented method print_only_names in StudentViewShortInfo")