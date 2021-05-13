from src.bib_items import Author, Book, BookCopy
from src.library import Library, LibraryManager
from src.reports import LibraryTxtReport


def run_example():
    my_library = Library()
    add_data_to_library(my_library)
    do_sth_in_library(my_library)
    my_report = LibraryTxtReport()

    my_manager = LibraryManager(my_library, my_report)
    my_manager.generate_report()


def do_sth_in_library(library):
    library.borrow_book(2)
    library.return_borrowed_book(2)
    library.borrow_book(2)
    library.return_borrowed_book(2)
    library.borrow_book(2)

    library.borrow_book(3)
    library.return_borrowed_book(3)


def add_data_to_library(library):
    author_1 = Author("Thomas", "Mann", 80)
    author_2 = Author("Szczepan", "Twardoch", 40)

    book_1 = Book("Czarodziejska góra", 800, author_1, 2)
    book_2 = Book("Jak nie zostałem poetą", 160, author_2, 1)

    book_copy_1 = BookCopy(1, book_1)
    book_copy_2 = BookCopy(2, book_1)
    book_copy_3 = BookCopy(3, book_2)
    book_copy_4 = BookCopy(4, book_2)

    library.add_book_copy(book_copy_1)
    library.add_book_copy(book_copy_2)
    library.add_book_copy(book_copy_3)
    library.add_book_copy(book_copy_4)


if __name__ == "__main__":
    run_example()
