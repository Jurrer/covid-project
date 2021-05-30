from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QWidget, QVBoxLayout, QTabWidget, QPushButton, \
    QGridLayout, QLineEdit, QLabel, QFormLayout, QGroupBox, QScrollArea
import numpy as np
from Wykres import Wykres
from dzialania_na_plikach import WczytajPlik
from exceptions import LimitPanstw
from matplotlib import pyplot as plt


class Okno(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        self.__prepare_window(width, height)

    def __prepare_window(self, width, height):
        self.setWindowTitle("CovidPlots")
        self.__set_window_in_center(width, height)
        self.__tabs_widget = TabsWidget(self, width, height)
        self.setCentralWidget(self.__tabs_widget)
        self.show()

    def __set_window_in_center(self, width, height):
        self.setGeometry(0, 0, width, height)
        id = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        srodek = QDesktopWidget().availableGeometry(id).center()
        top_left = QPoint(srodek.x() - width / 2, srodek.y() - height / 2)
        self.move(top_left)


class TabsWidget(QWidget):

    def __init__(self, parent, width, height):
        super().__init__(parent)
        layout = QGridLayout()
        self.__tabs = QTabWidget()
        self.__tabs.resize(width, height)
        # self.__tab1 = TabInside()
        # self.__tab2 = TabInside()

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
        self.__countries_data = dict()
        self.__panstwa = PointsTab([], self)
        self.__lista_wybranych_krajow = self.__panstwa.get_lista_wybranych()
        self.__wyszukiwarka = QLineEdit("Szukaj...")
        self.__bledy = QLineEdit("Chwilowo brak błędu...")
        self.__bledy.setStyleSheet("background-color: whitesmoke;")
        QLineEdit.setReadOnly(self.__bledy, True)
        self.__bledy.setAlignment(QtCore.Qt.AlignCenter)
        self.__button1 = QPushButton("wczytaj plik")
        self.__button2 = QPushButton("tutaj bedzie suwak")
        self.__button3 = QPushButton("tutaj bedzie drugi suwak")
        self.__button4 = QPushButton("eksportuj do pdf")
        self.__button5 = QPushButton("resetuj")
        self.__button6 = QPushButton("dziennie/(CAŁKOWICIE)")
        self.__wykres = Wykres(self.__countries_data, self.__lista_wybranych_krajow, self.__daily_or_total,
                               self.__patients_or_cured)
        self.__layout.addWidget(self.__wykres, 1, 0, 7, 4)
        self.__layout.addWidget(self.__bledy, 0, 0, 1, 2)
        self.__layout.addWidget(self.__wyszukiwarka, 0, 4, 1, 2)
        self.__layout.addWidget(self.__panstwa, 1, 4, 2, 2)
        self.__layout.addWidget(self.__button1, 3, 4, 1, 2)
        self.__layout.addWidget(self.__button2, 4, 4, 1, 2)
        self.__layout.addWidget(self.__button3, 5, 4, 1, 2)
        self.__layout.addWidget(self.__button4, 6, 4, 1, 2)
        self.__layout.addWidget(self.__button5, 7, 4, 1, 2)
        self.__layout.addWidget(self.__button6, 8, 4, 1, 2)

        self.setLayout(self.__layout)
        self.__button1.clicked.connect(self.__btn1)
        self.__wyszukiwarka.textEdited.connect(self.__wyszukaj)
        self.__button2.clicked.connect(self.__wypisz)
        self.__button3.clicked.connect(lambda _: print(self.__daily_or_total))
        self.__button6.clicked.connect(self.__change_DOT())
        self.__button5.clicked.connect(self.__aktualizuj_okno)

    def __aktualizuj_okno(self):
        self.__lista_wybranych_krajow.clear()
        self.make_graph()
        self.__panstwa.usun_wszystko()
        self.error_change(None)
        self.__wyszukiwarka.setText("Szukaj...")


    def set_lista_wybranych_krajow(self, arg):
        self.__lista_wybranych_krajow = arg

    def __init_POC(self):
        if self.__tab_name == "Zachorowania":
            patients_or_cured = "patients"
        elif self.__tab_name == "Ozdrowienia":
            patients_or_cured = "cured"
        return patients_or_cured

    def __change_DOT(self):
        return lambda _: self.__changedot()

    def __changedot(self):
        if self.__daily_or_total == "total":
            self.__daily_or_total = "daily"
            self.__button6.setText("(DZIENNIE)/calkowicie")
            self.make_graph()
        elif self.__daily_or_total == "daily":
            self.__daily_or_total = "total"
            self.__button6.setText("dziennie/(CAŁKOWICIE)")

            self.make_graph()

    def make_graph(self):
        self.__wykres = Wykres(self.__countries_data, self.__lista_wybranych_krajow, self.__daily_or_total,
                               self.__patients_or_cured)
        self.__layout.addWidget(self.__wykres, 1, 0, 7, 4)
        self.setLayout(self.__layout)

    def __btn1(self):
        file = WczytajPlik()
        self.error_change(file.blad)
        self.__countries_data = file.get_countries_data()
        if self.__countries_data:
            self.__panstwa = PointsTab(list(self.__countries_data.keys()), self)
            self.__layout.addWidget(self.__panstwa, 1, 4, 2, 2)

    def error_change(self, error):
        if error:
            self.__bledy.setStyleSheet("background-color: tomato;")
            self.__bledy.clear()
            self.__bledy.setText(error)
        else:
            self.__bledy.setStyleSheet("background-color: whitesmoke;")
            self.__bledy.clear()
            self.__bledy.setText("Chwilowo brak błędu...")

    def __wyszukaj(self):
        self.__panstwo = self.__wyszukiwarka.text()
        print(self.__panstwo)
        if not self.__panstwo:
            self.__panstwa.reset()
        elif len(self.__panstwo) == 1:
            self.__panstwa.search_by_letter(self.__panstwo)
        else:
            self.__panstwa.search(self.__panstwo)

    def __wypisz(self):
        print(self.__lista_wybranych_krajow)


class PointsTab(QScrollArea):
    def __init__(self, names, przyciski: Przyciski):
        super().__init__()
        self.__names = names
        self.__lista_wybranych = list()
        self.__init_view(names)
        self.blad = None
        self.przyciski = przyciski

    def search(self, name):
        self.__change_view(name)

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

    def reset(self):
        self.__init_view(self.__names)

    def __choose_country(self, btn, name):
        return lambda _: self.__ogarnij_wybieranie(btn, name)

    def __ogarnij_wybieranie(self, btn, name):
        if name not in self.__lista_wybranych:
            try:
                if len(self.__lista_wybranych) >= 6:
                    raise LimitPanstw
                else:
                    self.__lista_wybranych.append(name)
                    self.przyciski.set_lista_wybranych_krajow(self.get_lista_wybranych())
                    self.przyciski.make_graph()
                    self.blad = None
                    self.przyciski.error_change(self.blad)
                    btn.setStyleSheet("background-color : lightgreen")
            except LimitPanstw as err:
                self.blad = str(err)
                self.przyciski.error_change(self.blad)
        else:
            self.__lista_wybranych.remove(name)
            self.przyciski.set_lista_wybranych_krajow(self.get_lista_wybranych())
            self.przyciski.make_graph()
            self.blad = None
            self.przyciski.error_change(self.blad)
            btn.setStyleSheet("background-color : ")

    def get_lista_wybranych(self):
        return self.__lista_wybranych

    def usun_wszystko(self):
        self.__names = []
        self.__init_view(self.__names)
