from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QWidget, QTabWidget, QPushButton, \
    QGridLayout, QLineEdit, QFormLayout, QGroupBox, QScrollArea
from Wykres import Wykres
from dzialania_na_plikach import WczytajPlik
from exceptions import LimitPanstw
from PDFGenerator import PdfSaveButton

class Okno(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        self.__prepare_window(width, height)

    def __prepare_window(self, width, height):
        self.setWindowTitle("CovidPlots")
        self.__set_window_in_center(width, height)
        self.__tabs_widget = Zakladki(self, width, height)
        self.setCentralWidget(self.__tabs_widget)
        self.show()

    def __set_window_in_center(self, width, height):
        self.setGeometry(0, 0, width, height)
        id = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        srodek = QDesktopWidget().availableGeometry(id).center()
        top_left = QPoint(srodek.x() - width / 2, srodek.y() - height / 2)
        self.move(top_left)


class Zakladki(QWidget):
    def __init__(self, parent, width, height):
        super().__init__(parent)
        layout = QGridLayout()
        self.__tabs = QTabWidget()
        self.__tabs.resize(width, height)

        self.__tabs.addTab(Przyciski("Zachorowania"), "Zachorowania")
        self.__tabs.addTab(Przyciski("Ozdrowienia"), "Ozdrowienia")

        layout.addWidget(self.__tabs)
        self.setLayout(layout)


class Przyciski(QWidget):
    def __init__(self, tab_name):
        super().__init__()
        self.__tab_name = tab_name
        self.__daily_or_total = "total"
        self.__layout = QGridLayout()
        self.__patients_or_cured = self.__init_POC()
        self.__errors_label = self.__init_errors_label()
        self.__countries_data = dict()
        self.__countries = PointsTab([], self)
        self.__choosed_countries = self.__countries.get_choosed_countries_list()
        self.__searcher = QLineEdit()
        self.__searcher.setPlaceholderText("Szukaj...")
        self.__button_load_file = QPushButton("wczytaj plik")
        self.__first_slider = QPushButton("tutaj bedzie suwak") #todo
        self.__second_slider = QPushButton("tutaj bedzie drugi suwak") #todo
        self.__button_reset = QPushButton("resetuj")
        self.__button_daily_total = QPushButton("dziennie/(CAŁKOWICIE)")
        self.__wykres = Wykres(self.__countries_data, self.__choosed_countries, self.__daily_or_total,
                               self.__patients_or_cured)
        self.__button_export_to_pdf = PdfSaveButton("eksportuj do pdf", self.__wykres)
        self.__add_buttons_to_layout()
        self.setLayout(self.__layout)

    def __init_errors_label(self):
        errors_label = QLineEdit("Chwilowo brak błędu...")
        errors_label.setStyleSheet("background-color: whitesmoke;")
        QLineEdit.setReadOnly(errors_label, True)
        errors_label.setAlignment(QtCore.Qt.AlignCenter)
        return errors_label

    def __add_buttons_to_layout(self):
        self.__layout.addWidget(self.__errors_label, 0, 0, 1, 2)
        self.__layout.addWidget(self.__wykres, 1, 0, 7, 4)
        self.__layout.addWidget(self.__searcher, 0, 4, 1, 2)
        self.__layout.addWidget(self.__countries, 1, 4, 2, 2)
        self.__layout.addWidget(self.__button_load_file, 3, 4, 1, 2)
        self.__layout.addWidget(self.__first_slider, 4, 4, 1, 2)
        self.__layout.addWidget(self.__second_slider, 5, 4, 1, 2)
        self.__layout.addWidget(self.__button_export_to_pdf, 6, 4, 1, 2)
        self.__layout.addWidget(self.__button_reset, 7, 4, 1, 2)
        self.__layout.addWidget(self.__button_daily_total, 8, 4, 1, 2)
        self.__button_load_file.clicked.connect(self.__btn1)
        self.__searcher.textEdited.connect(self.__wyszukaj)
        self.__first_slider.clicked.connect(self.__wypisz) #todo
        self.__second_slider.clicked.connect(lambda _: print(self.__daily_or_total)) #todo
        self.__button_daily_total.clicked.connect(self.__change_DOT())
        self.__button_reset.clicked.connect(self.__clear_window)

    def __clear_window(self):
        self.__choosed_countries.clear()
        self.make_graph()
        self.__countries.reset()
        self.error_change(None)
        self.__searcher.setText("")


    def set_choosed_countries(self, arg):
        self.__choosed_countries = arg

    def __init_POC(self):
        if self.__tab_name == "Zachorowania":
            patients_or_cured = "patients"
        elif self.__tab_name == "Ozdrowienia":
            patients_or_cured = "cured"
        else:
            patients_or_cured = "patients/cured"
        return patients_or_cured

    def __change_DOT(self):
        return lambda _: self.__changedot()

    def __changedot(self):
        if self.__daily_or_total == "total":
            self.__daily_or_total = "daily"
            self.__button_daily_total.setText("(DZIENNIE)/calkowicie")
            self.make_graph()
        elif self.__daily_or_total == "daily":
            self.__daily_or_total = "total"
            self.__button_daily_total.setText("dziennie/(CAŁKOWICIE)")
            self.make_graph()
        else:
            pass

    def make_graph(self):
        self.__wykres = Wykres(self.__countries_data, self.__choosed_countries, self.__daily_or_total,
                               self.__patients_or_cured)
        self.__button_export_to_pdf = PdfSaveButton("eksportuj do pdf", self.__wykres)
        self.__layout.addWidget(self.__wykres, 1, 0, 7, 4)
        self.__layout.addWidget(self.__button_export_to_pdf, 6, 4, 1, 2)

    def __btn1(self):
        file = WczytajPlik()
        self.error_change(file.blad)
        self.__countries_data = file.get_countries_data()
        if self.__countries_data:
            self.__countries = PointsTab(list(self.__countries_data.keys())[1:], self)
            self.__layout.addWidget(self.__countries, 1, 4, 2, 2)

    def error_change(self, error):
        if error:
            self.__errors_label.setStyleSheet("background-color: tomato;")
            self.__errors_label.clear()
            self.__errors_label.setText(error)
        else:
            self.__errors_label.setStyleSheet("background-color: whitesmoke;")
            self.__errors_label.clear()
            self.__errors_label.setText("Chwilowo brak błędu...")

    def __wyszukaj(self):
        self.__panstwo = self.__searcher.text()
        if not self.__panstwo:
            self.__countries.reset()
        elif len(self.__panstwo) == 1:
            self.__countries.search_by_letter(self.__panstwo)
        else:
            self.__countries.search(self.__panstwo)

    def __wypisz(self):
        print(self.__choosed_countries)


class PointsTab(QScrollArea):
    def __init__(self, names, przyciski: Przyciski):
        super().__init__()
        self.__names = names
        self.__lista_wybranych = list()
        self.__init_view(names)
        self.__blad = None
        self.__przyciski = przyciski

    def search(self, name):
        self.__change_view(name)

    def get_choosed_countries_list(self):
        return self.__lista_wybranych

    def reset(self):
        self.__init_view(self.__names)

    def __make_button(self, name, btn_layout):
        btnname = name
        btn = QPushButton(btnname)
        btn.clicked.connect(self.__choose_country(btn, btnname))
        self.__ustaw_kolory(btn, btnname)
        btn_layout.addRow(btn)

    def __add_buttons_to_layout(self, btn_group, btn_layout):
        btn_group.setLayout(btn_layout)
        self.setWidget(btn_group)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)

    def __init_view(self, names):
        btn_layout = QFormLayout()
        btn_group = QGroupBox()

        for name in names:
            self.__make_button(name, btn_layout)
        self.__add_buttons_to_layout(btn_group, btn_layout)

    def __change_view(self, country):
        btn_layout = QFormLayout()
        btn_group = QGroupBox()
        country = country.upper()
        tmp = 0
        for name in self.__names:
            name_copy = name.upper()
            if len(name) >= len(country):
                for i in range(len(country)):
                    if country[i] == name_copy[i]:
                        tmp = 1
                    else:
                        tmp = 0
                        break
                if tmp != 0:
                    self.__make_button(name, btn_layout)
        self.__add_buttons_to_layout(btn_group, btn_layout)

    def search_by_letter(self, letter):
        letter = letter.upper()
        names = self.__names
        btn_layout = QFormLayout()
        btn_group = QGroupBox()

        for name in names:
            if name[0] == letter:
                self.__make_button(name, btn_layout)
        self.__add_buttons_to_layout(btn_group, btn_layout)

    def __ustaw_kolory(self, btn, btnname):
        if btnname in self.__lista_wybranych:
            btn.setStyleSheet("background-color : lightgreen")
        else:
            btn.setStyleSheet("background-color : ")


    def __choose_country(self, btn, name):
        return lambda _: self.__ogarnij_wybieranie(btn, name)

    def __ogarnij_wybieranie(self, btn, name):
        if name not in self.__lista_wybranych:
            try:
                if len(self.__lista_wybranych) >= 6:
                    raise LimitPanstw
                else:
                    self.__lista_wybranych.append(name)
                    self.__przyciski.set_choosed_countries(self.get_choosed_countries_list())
                    self.__przyciski.make_graph()
                    self.__blad = None
                    self.__przyciski.error_change(self.__blad)
                    btn.setStyleSheet("background-color : lightgreen")
            except LimitPanstw as err:
                self.__blad = str(err)
                self.__przyciski.error_change(self.__blad)
        else:
            self.__lista_wybranych.remove(name)
            self.__przyciski.set_choosed_countries(self.get_choosed_countries_list())
            self.__przyciski.make_graph()
            self.__blad = None
            self.__przyciski.error_change(self.__blad)
            btn.setStyleSheet("background-color : ")

