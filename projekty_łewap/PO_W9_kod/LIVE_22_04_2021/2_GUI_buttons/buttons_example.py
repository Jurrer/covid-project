import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout


class ButtonView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Button view")
        width, height = 300, 150
        self.setFixedSize(width, height)

        click_me_btn = QPushButton("Please, click me now!")
        click_me_btn.clicked.connect(self.__print_hello)

        layout = QVBoxLayout()
        layout.addWidget(click_me_btn)
        self.setLayout(layout)

        self.show()

    def __print_hello(self):
        print("Come with me now!")


if __name__ == "__main__":
    app = QApplication([])

    button_view = ButtonView()

    sys.exit(app.exec_())
