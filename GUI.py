from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QWidget, QVBoxLayout, QTabWidget, QPushButton, \
    QGridLayout, QLineEdit, QLabel, QFormLayout, QGroupBox, QScrollArea
import numpy as np

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

        self.__tabs.addTab(Przyciski(), "Zachorowania")
        self.__tabs.addTab(Przyciski(), "Ozdrowienia")

        layout.addWidget(self.__tabs)
        self.setLayout(layout)


class Przyciski(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.countries_data = dict()
        self.panstwa = PointsTab([], self)
        self.lista_wybranych_krajow = self.panstwa.get_lista_wybranych()
        self.wyszukiwarka = QLineEdit("Szukaj...")
        self.bledy = QLineEdit("Chwilowo brak błędu...")
        self.bledy.setStyleSheet("background-color: whitesmoke;")
        QLineEdit.setReadOnly(self.bledy, True)
        self.bledy.setAlignment(QtCore.Qt.AlignCenter)
        self.button1 = QPushButton("wczytaj plik")
        self.button2 = QPushButton("tutaj bedzie suwak")
        self.button3 = QPushButton("tutaj bedzie drugi suwak")
        self.button4 = QPushButton("eksportuj do pdf")
        self.button5 = QPushButton("resetuj")
        # self.button6 = QPushButton("dziennie/calkowicie")
        self.wykres = QLabel()
        self.layout.addWidget(self.wykres, 1, 0, 7, 4)
        self.layout.addWidget(self.bledy, 0, 0, 1, 2)
        self.layout.addWidget(self.wyszukiwarka, 0, 4, 1, 2)
        self.layout.addWidget(self.panstwa, 1, 4, 2, 2)
        self.layout.addWidget(self.button1, 3, 4, 1, 2)
        self.layout.addWidget(self.button2, 4, 4, 1, 2)
        self.layout.addWidget(self.button3, 5, 4, 1, 2)
        self.layout.addWidget(self.button4, 6, 4, 1, 2)
        self.layout.addWidget(self.button5, 7, 4, 1, 2)
        # self.layout.addWidget(self.button6, 8, 4, 1, 2)

        self.setLayout(self.layout)
        self.button1.clicked.connect(self.__btn1)
        self.wyszukiwarka.textEdited.connect(self.__wyszukaj)
        self.button2.clicked.connect(self.__wypisz)
        self.button3.clicked.connect(self.suwak1())
    def __daily(self):
        daily = dict()
        for key in self.countries_data.keys():
            daily[key] = self.__lista_roznic(self.countries_data[key])
        return daily

    def __lista_roznic(self, lista):
        listab = list()
        for i in range(len(lista)):
            if i == 0:
                listab.append(0)
            else:
                listab.append(lista[i]-lista[i-1])
        return listab

    def suwak1(self):
        return lambda _: self.display_data(self.countries_data)

    def display_data(self, countries_data):
        print(self.lista_wybranych_krajow)
        for country in self.lista_wybranych_krajow:
            X = np.arange(0, len(countries_data[country]), 1)
            plt.semilogy(X, self.countries_data[country], label=country)
            print(country)
            print(countries_data[country])
            print(len(countries_data[country]))

        plt.xlabel("Days (subsequent data)")
        plt.ylabel("Total number of patients")
        plt.title("Covid-19 number of patients since 01.01.2020")
        plt.grid()
        plt.legend(loc="lower right")
        plt.tight_layout()
        plt.show()

    def __btn1(self):
        file = WczytajPlik()
        self.error_change(file.blad)
        self.countries_data = file.get_countries_data()
        self.countries_data_daily = self.__daily()
        print(len(self.countries_data_daily["Argentina"]))
        print(len(self.countries_data["Argentina"]))
        # print(self.countries_data)
        if self.countries_data:
            self.panstwa = PointsTab(list(self.countries_data.keys()), self)
            self.layout.addWidget(self.panstwa, 1, 4, 2, 2)

    def error_change(self, error):
        if error:
            self.bledy.setStyleSheet("background-color: tomato;")
            self.bledy.clear()
            self.bledy.setText(error)
        else:
            self.bledy.setStyleSheet("background-color: whitesmoke;")
            self.bledy.clear()
            self.bledy.setText("Chwilowo brak błędu...")

    def __wyszukaj(self):
        self.panstwo = self.wyszukiwarka.text()
        print(self.panstwo)
        if not self.panstwo:
            self.panstwa.reset()
        elif len(self.panstwo) == 1:
            self.panstwa.search_by_letter(self.panstwo)
        else:
            self.panstwa.search(self.panstwo)

    def __usun(self):
        self.wyszukiwarka.clear()

    def __wypisz(self):
        # self.lista_wybranych_krajow = self.panstwa.get_lista_wybranych()
        # print(self.countries_data)
        print(self.lista_wybranych_krajow)


class PointsTab(QScrollArea):
    def __init__(self, names, cos: Przyciski):
        super().__init__()
        self.names = names
        self.lista_wybranych = list()
        self.__init_view(names)
        self.blad = None
        self.cos = cos

    def search(self, name):
        self.__change_view(name)

    def __init_view(self, names):
        btn_layout = QFormLayout()
        btn_group = QGroupBox()

        for name in names:
            btnname = name
            btn = QPushButton(btnname)
            btn.clicked.connect(self.__choose_country(btn, btnname))
            self.__ustaw_kolory(btn, btnname)
            btn_layout.addRow(btn)

        btn_group.setLayout(btn_layout)
        self.setWidget(btn_group)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)

    def __change_view(self, country):
        btn_layout = QFormLayout()
        btn_group = QGroupBox()
        country = country.upper()

        tmp = 0

        for name in self.names:
            name_copy = name.upper()
            if len(name) >= len(country):
                for i in range(len(country)):
                    if country[i] == name_copy[i]:
                        tmp = 1
                    else:
                        tmp = 0
                        break
                if tmp != 0:
                    btnname = name
                    btn = QPushButton(btnname)
                    btn.clicked.connect(self.__choose_country(btn, btnname))
                    self.__ustaw_kolory(btn, btnname)
                    btn_layout.addRow(btn)

        btn_group.setLayout(btn_layout)
        self.setWidget(btn_group)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)

    def search_by_letter(self, letter):
        letter = letter.upper()
        # print(letter)
        names = self.names
        btn_layout = QFormLayout()
        btn_group = QGroupBox()

        for name in names:
            if name[0] == letter:
                btnname = name
                btn = QPushButton(btnname)
                btn.clicked.connect(self.__choose_country(btn, btnname))
                self.__ustaw_kolory(btn, btnname)
                btn_layout.addRow(btn)

        btn_group.setLayout(btn_layout)
        self.setWidget(btn_group)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)

    def __ustaw_kolory(self, btn, btnname):
        if btnname in self.lista_wybranych:
            btn.setStyleSheet("background-color : lightgreen")
        else:
            btn.setStyleSheet("background-color : ")

    def reset(self):
        self.__init_view(self.names)

    def __choose_country(self, btn, name):
        return lambda _: self.__ogarnij_wybieranie(btn, name)

    def __ogarnij_wybieranie(self, btn, name):
        if name not in self.lista_wybranych:
            try:
                if len(self.lista_wybranych) >= 6:
                    raise LimitPanstw
                else:
                    self.lista_wybranych.append(name)
                    self.cos.lista_wybranych_krajow = self.get_lista_wybranych()
                    print(self.lista_wybranych)
                    self.blad = None
                    self.cos.error_change(self.blad)
                    btn.setStyleSheet("background-color : lightgreen")
            except LimitPanstw as err:
                self.blad = str(err)
                self.cos.error_change(self.blad)
        else:
            self.lista_wybranych.remove(name)
            self.cos.lista_wybranych_krajow = self.get_lista_wybranych()
            print(self.lista_wybranych)
            self.blad = None
            self.cos.error_change(self.blad)
            btn.setStyleSheet("background-color : ")
        # print(self.lista_wybranych)

    def get_lista_wybranych(self):
        return self.lista_wybranych
