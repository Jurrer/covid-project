from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QWidget, QVBoxLayout, QTabWidget, QPushButton, \
    QGridLayout


class Okno(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        self.setWindowTitle("CovidPlots")
        self.__set_window_in_center(width, height)
        layout = QGridLayout()
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
        layout = QVBoxLayout()

        self.__tabs = QTabWidget()
        self.__tabs.resize(width, height)

        self.__tab1 = QWidget()
        self.__tab2 = QWidget()

        self.__tabs.addTab(self.__tab1, "Zachorowania")
        self.__tabs.addTab(self.__tab2, "Ozdrwienia")

        self.__tab1.setLayout(QVBoxLayout(self))
        self.__tab2.setLayout(QVBoxLayout(self))

        layout.addWidget(self.__tabs)
        self.setLayout(layout)
class Button(QPushButton):
    def __init__(self, name):
        self.__name = name
