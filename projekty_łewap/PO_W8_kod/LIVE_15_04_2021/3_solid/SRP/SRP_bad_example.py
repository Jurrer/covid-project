class Student:

    def __init__(self, name, surname, age):
        self.__name = name
        self.__surname = surname
        self.__age = age
        self.__registration_validity_date = self.__initialize_registration_for_one_year()
        self.__annex_signed = False

    def __initialize_registration_for_one_year(self): pass

    def check_registration(self): pass

    def enroll_for_next_semester_if_all_is_correct(self): pass

    def save_to_file(self): pass
