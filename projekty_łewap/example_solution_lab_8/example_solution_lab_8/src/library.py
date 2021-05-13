from src.bib_items import BookCopyNotFoundException, BookCopyCurrentlyAvailableException, \
    BookCopyUnavailableException, BookCopyCurrentlyExistsException


class Library:

    def __init__(self):
        self.__copies_of_books = []

    def add_book_copy(self, book_copy):
        if book_copy not in self.__copies_of_books:
            self.__copies_of_books.append(book_copy)
        else:
            raise BookCopyCurrentlyExistsException("book_copy_id: {}".format(book_copy.get_book_copy_id()))

    def borrow_book(self, book_copy_id):
        book_copy = self.__find_book_copy_by_id(book_copy_id)
        if book_copy.is_available():
            book_copy.set_unavailable()
            return book_copy
        else:
            raise BookCopyUnavailableException("book_copy_id: {}".format(book_copy.get_book_copy_id()))

    def return_borrowed_book(self, book_copy_id):
        book_copy = self.__find_book_copy_by_id(book_copy_id)
        if book_copy.is_unavailable():
            book_copy.increase_loan_counter()
            book_copy.set_available()
        else:
            raise BookCopyCurrentlyAvailableException("book_copy_id: {}".format(book_copy.get_book_copy_id()))

    def __find_book_copy_by_id(self, book_copy_id):
        for book_copy in self.__copies_of_books:
            if book_copy.get_book_copy_id() == book_copy_id:
                return book_copy
        raise BookCopyNotFoundException("book_copy_id: {}".format(book_copy_id))

    def get_copies_of_books(self):
        return self.__copies_of_books


class LibraryManager:
    def __init__(self, library, report):
        self.__library = library
        self.__report = report

    def get_library(self):
        return self.__library

    def generate_report(self):
        data = self.__library.get_copies_of_books()
        self.__report.prepare_full_report(data)
