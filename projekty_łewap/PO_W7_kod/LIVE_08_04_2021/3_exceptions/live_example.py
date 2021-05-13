from exceptions_classes import InvalidStudentParamsException
from student import Student


def main():
    try:
        stud_1 = Student("")
    except InvalidStudentParamsException as err:
        print(f"Caught error: {err}")


if __name__ == "__main__":
    main()
