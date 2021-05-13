import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QTableView, QHeaderView, QVBoxLayout
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class AppDemo(QWidget):
    def __init__(self, companies):
        super().__init__()
        self.resize(1200, 1000)
        mainLayout = QVBoxLayout()
        self.__companies = companies
        model = QStandardItemModel(len(self.__companies), 1)
        model.setHorizontalHeaderLabels(['Company'])
        for row, company in enumerate(self.__companies):
            item = QStandardItem(company)
            model.setItem(row, 0, item)
        filter_proxy_model = QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(model)
        filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(0)
        search_field = QLineEdit()
        search_field.setStyleSheet('font-size: 35px; height: 60px;')
        search_field.textChanged.connect(filter_proxy_model.setFilterRegExp)
        mainLayout.addWidget(search_field)
        table = QTableView()
        table.setStyleSheet('font-size: 35px;')
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setModel(filter_proxy_model)
        mainLayout.addWidget(table)
        self.setLayout(mainLayout)

def read_countries_data(filepath, countries):
    countries_data = dict()

    with open(filepath, "r") as f:
        for line in f:
            maybe_country = line.split(",")[COUNTRY_COLUMN_ID]

            if maybe_country in countries:
                line = line.strip()
                n_of_patients_in_time = get_patients_as_vector(line)

                countries_data[maybe_country] = n_of_patients_in_time

    return countries_data


countries_data = read_countries_data(filepath, countries)

app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())