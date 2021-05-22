from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QWidget, QVBoxLayout, QTabWidget, QPushButton, \
    QGridLayout, QLineEdit, QLabel, QFormLayout, QGroupBox, QScrollArea

from dzialania_na_plikach import WczytajPlik
from exceptions import LimitPanstw


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
        self.wyszukiwarka = QLineEdit("SZUKAJ...")
        self.bledy = QLineEdit("Chwilowo brak błędu...")
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
    def __btn1(self):
        file = WczytajPlik()
        self.error_change(file.blad)
        self.countries_data = file.get_countries_data()
        if self.countries_data:
            self.panstwa = PointsTab(list(self.countries_data.keys()), self)
            self.layout.addWidget(self.panstwa, 1, 4, 2, 2)

    def error_change(self, error):
        self.bledy.clear()
        self.bledy.setText("Chwilowo brak błędu...")
        if error:
            self.bledy.clear()
            self.bledy.setText(error)

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



class PointsTab(QScrollArea):
    def __init__(self, names, cos: Przyciski):
        super().__init__()
        self.names = names
        self.__init_view(names)
        self.lista_wybranych = []
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
            btn.clicked.connect(self.__choose_country(btnname))
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
                    btn.clicked.connect(self.__choose_country(btnname))
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
                btn.clicked.connect(self.__choose_country(btnname))
                btn_layout.addRow(btn)

        btn_group.setLayout(btn_layout)
        self.setWidget(btn_group)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)

    def reset(self):
        self.__init_view(self.names)

    def __choose_country(self, name):
        return lambda _: self.__ogarnij_wybieranie(name)

    def __ogarnij_wybieranie(self, name):
        if name not in self.lista_wybranych:
            try:
                if len(self.lista_wybranych) >= 6:
                    raise LimitPanstw
                else:
                    self.lista_wybranych.append(name)
                    self.blad = None
                    self.cos.error_change(self.blad)
            except LimitPanstw as err:
                self.blad = str(err)
                self.cos.error_change(self.blad)
        else:
            self.lista_wybranych.remove(name)
            self.blad = None
            self.cos.error_change(self.blad)
        print(self.lista_wybranych)

    def get_lista_wybranych(self):
        return self.lista_wybranych
