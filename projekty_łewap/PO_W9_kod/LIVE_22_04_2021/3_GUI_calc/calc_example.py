import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QGroupBox, QPushButton, QVBoxLayout


class CalcButton(QPushButton):
    def __init__(self, value, text_panel: QLineEdit):
        super().__init__(value)
        self.__value = value
        self.__text_panel = text_panel

        self.clicked.connect(self.__update_text_field)

    def __update_text_field(self):
        org_text = self.__text_panel.text()
        org_text = "" if org_text == "." else org_text

        new_text = f"{org_text}{self.__value}"
        self.__text_panel.setText(new_text)


class CalcEqButton(QPushButton):
    def __init__(self, value, text_field: QLineEdit):
        super().__init__(value)
        self.__value = value
        self.__text_field = text_field

        self.clicked.connect(self.__count_result)

    def __count_result(self):
        new_text = f"ERROR Not implemented!"
        self.__text_field.setText(new_text)


class CalcTextPanel(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setAlignment(QtCore.Qt.AlignRight)
        self.setReadOnly(True)
        self.setText(".")


class CalcNumsPanel(QGroupBox):
    def __init__(self, text_panel):
        super().__init__()
        self.__text_panel = text_panel
        self.__prepare_numbers_buttons_grid()

    def __prepare_numbers_buttons_grid(self):
        self.__create_nums_buttons()
        layout = QGridLayout()

        layout.addWidget(self.__btn_1, 0, 0)
        layout.addWidget(self.__btn_2, 0, 1)

        self.setLayout(layout)

    def __create_nums_buttons(self):
        self.__btn_1 = CalcButton("1", self.__text_panel)
        self.__btn_2 = CalcButton("2", self.__text_panel)


class CalcMathsPanel(QGroupBox):
    def __init__(self, text_panel):
        super().__init__()
        self.__text_panel = text_panel

        self.__prepare_math_buttons_grid()

    def __prepare_math_buttons_grid(self):
        self.__create_math_buttons()
        layout = QVBoxLayout()

        layout.addWidget(self.__btn_plus)
        layout.addWidget(self.__btn_eq)

        self.setLayout(layout)

    def __create_math_buttons(self):
        self.__btn_plus = CalcButton("+", self.__text_panel)
        self.__btn_eq = CalcEqButton("=", self.__text_panel)


class CalcWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.__prepare_window()

    def __prepare_window(self):
        self.__text_panel = CalcTextPanel()
        self.__nums_buttons_box = CalcNumsPanel(self.__text_panel)
        self.__math_buttons_box = CalcMathsPanel(self.__text_panel)

        main_layout = QGridLayout()
        main_layout.addWidget(self.__text_panel, 0, 0, 1, 2)
        main_layout.addWidget(self.__nums_buttons_box, 1, 0)
        main_layout.addWidget(self.__math_buttons_box, 1, 1)

        self.setLayout(main_layout)
        self.show()


if __name__ == "__main__":
    app = QApplication([])

    calc_window = CalcWindow()

    sys.exit(app.exec_())
