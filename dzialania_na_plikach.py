from PyQt5.QtWidgets import QFileDialog

from exceptions import ZlyFormatPliku


class WczytajPlik(QFileDialog):
    def __init__(self):
        super().__init__()
        self.blad = None
        filename = self.__open_file()
        self.__test_filename(filename)

    def get_countries_data(self):
        return self.countries_data

    def __open_file(self):
        try:
            filename = QFileDialog.getOpenFileName()[0]
            if filename.split(".")[-1] != "csv":
                raise ZlyFormatPliku
            self.countries_data = self.__load_data(filename)
        except ZlyFormatPliku as err:
            self.blad = str(err)
            self.countries_data = None

        return filename

    def __test_filename(self, filename):
        print(filename)

    def __load_data(self, filename):
        column = 4
        lista_krajow = list()
        lista_pacjentow = list()

        with open(filename, "r") as f:
            for line in f:
                country_name = line.split(",")[1]
                lista_krajow.append(country_name)
                line = line.strip()
                patients = line.split(",")[column:]
                lista_pacjentow.append(patients)
            countries_data = self.__sumuj_przebiegi(lista_krajow, lista_pacjentow)

        return countries_data


    def __sumuj_przebiegi(self, names, values):
        data = dict()
        iterator = 1
        country_value = list()
        for name in names[1:]:
            if iterator < len(names) - 1:
                next_name = names[iterator + 1]
                if next_name == name:
                    country_value = self.__sumuj_listy(country_value, values[iterator])
                elif next_name != name:
                    country_value = self.__sumuj_listy(country_value, values[iterator])
                    data[name] = country_value
                    country_value = list()
                iterator += 1
            else:
                country_value = self.__sumuj_listy(country_value, values[iterator])
                data[name] = country_value
                country_value = list()
        return data

    def __sumuj_listy(self, listaa, listab):
        value = list()
        if len(listaa) > 0:
            for i in range(len(listaa)):
                v = abs(int(float(listaa[i]))) + abs(int(float(listab[i])))
                value.append(v)
        elif len(listaa) == 0:
            for i in range(len(listab)):
                v = abs(int(float(listab[i])))
                value.append(v)
        return value