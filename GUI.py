from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QWidget, QVBoxLayout, QTabWidget, QPushButton, \
    QGridLayout, QLineEdit, QLabel, QFormLayout, QGroupBox, QScrollArea


class Okno(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        self.__prepare_window(width, height)

    def __prepare_window(self, width, height):
        self.setWindowTitle("CovidPlots")
        self.__set_window_in_center(width, height)
        main_layout = QGridLayout()
        self.__tabs_widget = TabsWidget(self, width, height)
        main_layout.addWidget(self.__tabs_widget)
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
        self.__tab1 = QTabWidget()
        self.__tab2 = QTabWidget()
        self.__tabs.addTab(self.__tab1, "Zachorowania")
        self.__tabs.addTab(self.__tab2, "Ozdrowienia")

        layout.addWidget(self.__tab1)
        layout.addWidget(self.__tab2)
        self.setLayout(layout)


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
            # btn.clicked.connect((lambda name_to_show: lambda _: print(name_to_show))(name))
            btn.clicked.connect(self.func_print_me(name))
            btn_layout.addRow(label, btn)

        btn_group.setLayout(btn_layout)
        self.setWidget(btn_group)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)

    def func_print_me(self, name):
        return lambda _: print(name)
