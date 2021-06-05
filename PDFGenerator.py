from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from Wykres import Wykres
from PyQt5.QtWidgets import QPushButton, QFileDialog
from reportlab.lib.utils import ImageReader

from exceptions import BrakPliku


class PdfReportGenerator:

    def __init__(self):
        self.__author = "Alek Jurrer and kapustekk"

    def create_and_save_report(self, img, filepath, pagesize=A4):
        pdf_template = self.__create_pdf_template(filepath, img, pagesize)
        pdf_template.setAuthor(self.__author)
        pdf_template.setTitle("")
        pdf_template.save()

    def __create_pdf_template(self, filepath, img, pagesize):
        canvas = Canvas(filepath, pagesize=pagesize)
        title_magic_offset, img_magic_offset = 50, 600
        title_x, title_y = A4[0] / 4, A4[1] - title_magic_offset
        img_x, img_y = 0, A4[1] - img_magic_offset
        title = f"Covid-plots by {self.__author} generated plot"
        canvas.drawString(title_x, title_y, title)
        canvas.drawImage(img, img_x, img_y, 550, 400)

        return canvas


class PdfSaveButton(QPushButton):
    def __init__(self, name, wykres, przyciski):
        super().__init__(name)
        self.__chart = wykres
        self.__pdf_generator = PdfReportGenerator()
        self.clicked.connect(self.__save_btn_action)
        self.przyciski = przyciski

    def __save_btn_action(self):
        img_data = self.__chart.get_img()
        img = ImageReader(img_data)

        try:
            filename = self.__prepare_file_chooser()
            if filename:  # tu miejsce na wgranie błędu
                self.blad = None
                self.przyciski.error_change(self.blad)
                filename = self.__zmien_filename(filename)
                self.__pdf_generator.create_and_save_report(img, filename)
            else:
                raise BrakPliku
        except BrakPliku as err:
            self.blad = str(err)
            self.przyciski.error_change(self.blad)

    def __prepare_file_chooser(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save PDF report", filter="All Files (*)")
        return filename

    def __zmien_filename(self, filename):
        name = filename.split("/")[-1]
        if "." in name:
            name2 = name.split(".")[0] + ".pdf"
        else:
            name2 = name + ".pdf"
        endfilename = filename.split("/")[:-1]
        endfilename2 = str()
        for element in endfilename:
            endfilename2 = endfilename2 + element + "/"
        endfilename2 = endfilename2 + name2

        return endfilename2
