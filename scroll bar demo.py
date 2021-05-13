import sys
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == "__main__":

    class EmptyWindow(QWidget):
        def __init__(self):
            super().__init__()
            width = 1260
            height = 680
            self.resize(width, height)
            self.setWindowTitle("Empty Window")
            self.show()

    if __name__ == "__main__":
        # print("Hello World")
        # print("Ez")
        app = QApplication([])

        empty_wyswietl = EmptyWindow()
        sys.exit(app.exec())
