from students.consts import VALID, INVALID
from students.deans_office import DeansOffice
from students.student import Student


def main():
    deans_office = DeansOffice()

    stud_1 = Student("Hans", "Castorp", 70, 456456, VALID)
    stud_2 = Student("Velvet", "Balsam", 63, 123789, INVALID)
    stud_3 = Student("Kubuś", "Puchatek", 91, 786111, VALID)

    deans_office.add_student(stud_1)
    deans_office.add_student(stud_2)
    deans_office.add_student(stud_3)

    # deans_office.remove_student(123789)
    # deans_office.remove_student(123789)
    deans_office.update_status(123789, VALID)

    deans_office.display_students()


if __name__ == "__main__":
    main()
