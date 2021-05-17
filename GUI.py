from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QWidget, QVBoxLayout, QTabWidget, QPushButton, \
    QGridLayout, QLineEdit, QLabel, QFormLayout, QGroupBox, QScrollArea

from dzialania_na_plikach import WczytajPlik
from exceptions import ZleDane


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

        self.__tabs.addTab(TabInside(), "Zachorowania")
        self.__tabs.addTab(TabInside(), "Ozdrowienia")

        layout.addWidget(self.__tabs)
        self.setLayout(layout)


class TabInside(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.countries_data = dict()
        self.panstwa = PointsTab([])
        self.wyszukiwarka = QLineEdit("SZUKAJ.........")
        self.bledy = QLineEdit("Chwilowo brak błędu...")
        QLineEdit.setReadOnly(self.bledy, True)
        self.bledy.setAlignment(QtCore.Qt.AlignCenter)
        self.button1 = QPushButton("wczytaj plik")
        self.button2 = QPushButton("tutaj bedzie suwak")
        self.button3 = QPushButton("tutaj bedzie drugi suwak")
        self.button4 = QPushButton("eksportuj do pdf")
        self.button5 = QPushButton("resetuj")
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

        self.setLayout(self.layout)
        self.button1.clicked.connect(self.__btn1)

    def __btn1(self):
        file = WczytajPlik()
        self.error_change(file.blad)
        self.countries_data = file.get_countries_data()
        if self.countries_data:
            self.panstwa = PointsTab(list(self.countries_data.keys()))
            self.layout.addWidget(self.panstwa, 1, 4, 2, 2)

    def error_change(self, error):
        self.bledy.clear()
        self.bledy.setText("Chwilowo brak błędu...")
        if error:
            self.bledy.clear()
            self.bledy.setText(error)

class PointsTab(QScrollArea):
    def __init__(self, names):
        super().__init__()
        self.__init_view(names)

    def __init_view(self, names):
        btn_layout = QFormLayout()
        btn_group = QGroupBox()

        for name in names:
            btnname = name
            label = QLabel(btnname)
            btn = QPushButton(btnname)
            btn.clicked.connect(self.func_print_me(btnname))
            btn_layout.addRow(btn)

        btn_group.setLayout(btn_layout)
        self.setWidget(btn_group)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)

    def func_print_me(self, name):
        return lambda _: print(name)
