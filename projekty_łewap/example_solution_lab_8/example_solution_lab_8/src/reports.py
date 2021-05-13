from datetime import datetime


class LibraryReport:
    def prepare_full_report(self, copies_of_books): pass


class LibraryTxtReport(LibraryReport):
    def __init__(self):
        self._report_filename = "book_report.txt"

    def prepare_full_report(self, copies_of_books):
        with open(self._report_filename, "w") as f:
            f.write("{}\n".format(str(datetime.now())))
            for book_copy in copies_of_books:
                book = book_copy.get_book()
                f.write("{} | {} | {}\n".format(book.get_title(), book.get_edition_id(), book_copy.get_loan_counter()))
