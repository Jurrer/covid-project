import sys

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QWidget, QTabWidget, QVBoxLayout, QScrollArea, \
    QFormLayout, QLabel, QPushButton, QGroupBox


class TabsApp(QMainWindow):

    def __init__(self, width, height):
        super().__init__()
        self.setWindowTitle("Tabs example app")
        self.__set_window_in_center(width, height)

        self.__tabs_widget = TabsWidget(self, width, height)
        self.setCentralWidget(self.__tabs_widget)
        self.show()

    def __set_window_in_center(self, width, height):
        self.setGeometry(0, 0, width, height)
        screen_id = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QDesktopWidget().availableGeometry(screen_id).center()
        top_left = QPoint(center_point.x() - width / 2, center_point.y() - height / 2)
        self.move(top_left)


class TabsWidget(QWidget):

    def __init__(self, parent, width, height):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.__tabs = QTabWidget()
        self.__tabs.resize(width, height)

        n_of_btns = 25
        self.__tab1 = PointsTab(n_of_btns)
        self.__tab2 = QWidget()

        self.__tabs.addTab(self.__tab1, "Tab 1")
        self.__tabs.addTab(self.__tab2, "Tab 2")

        self.__tab1.setLayout(QVBoxLayout(self))
        self.__tab2.setLayout(QVBoxLayout(self))

        layout.addWidget(self.__tabs)
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


if __name__ == "__main__":
    app = QApplication([])

    width, height = 600, 400
    tabs_app = TabsApp(width, height)

    sys.exit(app.exec_())
