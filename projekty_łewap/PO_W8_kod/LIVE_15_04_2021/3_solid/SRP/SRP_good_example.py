class Student:

    def __init__(self, name, surname, age):
        self.__name = name
        self.__surname = surname
        self.__age = age
        self.__registration_validity_date = self.__initialize_registration_for_one_year()
        self.__annex_signed = False

    # getters & setters

    def __initialize_registration_for_one_year(self): pass


class StudentRegistration:

    def enroll_for_next_semester_if_all_is_correct(self, student): pass

    def __check_registration(self, student): pass


class StudentRanking:

    def count_ranking(self, student): pass

    def __check_registration(self, student): pass

    def __count_mid_grade(self, student): pass


class StudentReport:

    def save_to_file(self, student): pass
