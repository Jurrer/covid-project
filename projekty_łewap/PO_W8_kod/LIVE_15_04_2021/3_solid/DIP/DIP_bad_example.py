class EmailReport:
    def send_email_report(self, data):
        pass

class PdfReport:
    pass

class AccountingStatistics:

    def summarize_the_last_month(self, last_month_data):
        # do sth
        email_report = EmailReport()
        email_report.send_email_report(last_month_data)