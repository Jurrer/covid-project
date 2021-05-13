import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QTableView, QHeaderView, QVBoxLayout
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import pandas as pd
import csv


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



filename = 'time_series_covid19_confirmed_global.csv'

with open(filename, newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

col_list = data[0]
df = pd.read_csv(filename, usecols=col_list)

countries = list(df["Country/Region"])

app = QApplication(sys.argv)
demo = AppDemo(countries)
demo.show()
sys.exit(app.exec_())
