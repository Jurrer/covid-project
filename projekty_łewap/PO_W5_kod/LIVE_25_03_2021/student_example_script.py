from students.consts import VALID, INVALID
from students.student import Student


def main():
    stud_1 = Student("Hans", "Castorp", 70, 456456, VALID)
    stud_2 = Student("Velvet", "Balsam", 63, 123789, INVALID)
    stud_3 = Student("Kubuś", "Puchatek", 91, 786111, VALID)

    print("-----------------")
    print(stud_1.name, stud_1.age, stud_1.album_id)
    print(stud_2.name, stud_2.age, stud_2.album_id)

    print(stud_1.to_dict())

    print("-----------------")
    print(stud_1)
    stud_1.update_status(INVALID)
    print(stud_1)

    print("-----------------")
    students = [stud_1, stud_2, stud_3]

    for stud in students:
        print(stud)


if __name__ == "__main__":
    main()
