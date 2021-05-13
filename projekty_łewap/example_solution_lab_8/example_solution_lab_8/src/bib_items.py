from enum import Enum, auto


class Author:
    def __init__(self, name, surname, age):
        self.__name = name
        self.__surname = surname
        self.__age = age

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname

    def get_age(self):
        return self.__age

    def __eq__(self, other):
        return self.__class__ == other.__class__ \
               and self.__dict__ == other.__dict__

    def __hash__(self):
        return self.__dict__.__hash__()


class BibItemStatus(Enum):
    AVAILABLE = auto()
    UNAVAILABLE = auto()


class BibItem:
    def __init__(self, title, num_of_pages, author):
        self.__title = title
        self.__num_of_pages = num_of_pages
        self.__author = author

    def get_title(self):
        return self.__title

    def get_num_of_pages(self):
        return self.__num_of_pages

    def get_author(self):
        return self.__author


class Book(BibItem):
    def __init__(self, title, num_of_pages, author, edition_id):
        super().__init__(title, num_of_pages, author)
        self.__edition_id = edition_id

    def get_edition_id(self):
        return self.__edition_id

    def __repr__(self):
        attrs = {k.split("__")[-1]: v for k, v in self.__dict__.items()}
        return str(attrs)

    def __eq__(self, other):
        return self.__class__ == other.__class__ \
               and self.__dict__ == other.__dict__

    def __hash__(self):
        return self.__dict__.__hash__()


class BookCopy:
    def __init__(self, book_copy_id, book):
        self.__book_copy_id = book_copy_id
        self.__book = book
        self.__loan_counter = 0
        self.__status = BibItemStatus.AVAILABLE

    def get_book_copy_id(self):
        return self.__book_copy_id

    def get_book(self):
        return self.__book

    def get_loan_counter(self):
        return self.__loan_counter

    def get_status(self):
        return self.__status

    def set_status(self, new_status):
        self.__status = new_status

    def is_available(self):
        return self.__status == BibItemStatus.AVAILABLE

    def is_unavailable(self):
        return self.__status == BibItemStatus.UNAVAILABLE

    def set_available(self):
        self.__status = BibItemStatus.AVAILABLE

    def set_unavailable(self):
        self.__status = BibItemStatus.UNAVAILABLE

    def increase_loan_counter(self):
        self.__loan_counter += 1

    def __eq__(self, other):
        return self.__class__ == other.__class__ \
               and self.__dict__ == other.__dict__

    def __hash__(self):
        return self.__dict__.__hash__()


class BookCopyNotFoundException(Exception):
    def __init__(self, msg):
        message = "The copy of book could not be found {%s}" % msg
        super().__init__(message)


class BookCopyUnavailableException(Exception):
    def __init__(self, msg):
        message = "The copy of book is unavailable {%s}" % msg
        super().__init__(message)


class BookCopyCurrentlyAvailableException(Exception):
    def __init__(self, msg):
        message = "The copy of the book is currently available {%s}" % msg
        super().__init__(message)


class BookCopyCurrentlyExistsException(Exception):
    def __init__(self, msg):
        message = "The copy of the book currently exists {%s}" % msg
        super().__init__(message)
