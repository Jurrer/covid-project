class MonthReport:
    def generate_report(self, data): pass


class EmailReport(MonthReport):

    def generate_report(self, data):
        # do sth
        self.__send_email_report(data)

    def __send_email_report(self, data):
        pass


class PdfReport(MonthReport):

    def generate_report(self, data):
        # do sth
        self.__save_to_file()

    def __save_to_file(self):
        pass


class AccountingStatistics:

    def __init__(self, month_report):
        self.__month_report = month_report

    def summarize_the_last_month(self, last_month_data):
        # do sth
        self.__month_report.generate_report(last_month_data)
