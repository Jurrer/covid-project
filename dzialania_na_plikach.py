from PyQt5.QtWidgets import QFileDialog


class WczytajPlik(QFileDialog):
    def __init__(self):
        super().__init__()
        filename = self.__open_file()
        self.__test_filename(filename)
        self.__load_data(filename)

    def __open_file(self):
        filename = QFileDialog.getOpenFileName()[0]
        return filename

    def __test_filename(self, filename):
        print(filename)

    def __load_data(self, filename):
        countries_data = dict()
        column = 4

        with open(filename, "r") as f:
            for line in f:
                country_name = line.split(",")[1]
                if country_name != "Country/Region":
                    line = line.strip()
                    patients = line.split(",")[column:]
                    countries_data[country_name] = patients

        print(countries_data)