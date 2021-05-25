# data from: https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases
import sys
from PyQt5.QtWidgets import QApplication
from GUI import Okno

if __name__ == "__main__":
    apk = QApplication([])

    width, height = 1260, 680
    tabs_app = Okno(width, height)

    sys.exit(apk.exec_())
