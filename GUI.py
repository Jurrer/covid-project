from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QWidget, QVBoxLayout, QTabWidget, QPushButton, \
    QGridLayout, QLineEdit, QLabel, QFormLayout, QGroupBox, QScrollArea

from dzialania_na_plikach import WczytajPlik


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
        self.__tab2 = TabInside()

        self.__tabs.addTab(TabInside(), "Zachorowania")
        self.__tabs.addTab(TabInside(), "Ozdrowienia")

        layout.addWidget(self.__tabs)
        self.setLayout(layout)


class TabInside(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.panstwa = PointsTab(25)
        self.wyszukiwarka = QLineEdit("SZUKAJ.........")
        self.bledy = QLineEdit("BLAD! MORDO TO MIAL BYC CSV")
        self.button1 = QPushButton("wczytaj plik")
        self.button2 = QPushButton("tutaj bedzie suwak")
        self.button3 = QPushButton("tutaj bedzie drugi suwak")
        self.button4 = QPushButton("eksportuj do pdf")
        self.button5 = QPushButton("resetuj")
        self.wykres = QLabel()
        layout.addWidget(self.wykres, 1, 0, 7, 4)
        layout.addWidget(self.bledy, 0, 0, 1, 2)
        layout.addWidget(self.wyszukiwarka, 0, 4, 1, 2)
        layout.addWidget(self.panstwa, 1, 4, 2, 2)
        layout.addWidget(self.button1, 3, 4, 1, 2)
        layout.addWidget(self.button2, 4, 4, 1, 2)
        layout.addWidget(self.button3, 5, 4, 1, 2)
        layout.addWidget(self.button4, 6, 4, 1, 2)
        layout.addWidget(self.button5, 7, 4, 1, 2)
        self.setLayout(layout)

        self.button1.clicked.connect(self.__btn1)

    def __btn1(self):
        WczytajPlik()


class PointsTab(QScrollArea):
    def __init__(self, size):
        super().__init__()
        self.__init_view(size)

    def __init_view(self, size):
        btn_layout = QFormLayout()
        btn_group = QGroupBox()

        for i in range(size):
            name = f"btn{i}"
            label = QLabel(name)
            btn = QPushButton(name)
            btn.clicked.connect(self.func_print_me(name))
            btn_layout.addRow(label, btn)

        btn_group.setLayout(btn_layout)
        self.setWidget(btn_group)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)

    def func_print_me(self, name):
        return lambda _: print(name)
