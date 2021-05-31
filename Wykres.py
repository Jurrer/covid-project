from io import BytesIO

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure



class Wykres(FigureCanvasQTAgg):
    def __init__(self, countries_data, countries_list, param, patients_or_cured, figsize=(7, 4), dpi=100):
        self.__fig = Figure(figsize=figsize, dpi=dpi)
        super().__init__(self.__fig)
        self.__countries_data = countries_data
        self.__countries_list = countries_list
        self.__param = param
        self.__patients_or_cured = patients_or_cured

        self.__init_fig()


    def get_img(self):
        image_data = BytesIO()
        self.__fig.savefig(image_data, format="png")
        image_data.seek(0)

        return image_data

    def __init_fig(self):
        self.__fig.add_subplot(111)
        self.__fig.suptitle(f"Covid-19 number of {self.__patients_or_cured} since 22.01.2020")
        self.__init_view()
        self.__fig.tight_layout()

    def __init_view(self):
        graph = self.__fig.axes[0]
        if self.__countries_data and self.__countries_list:
            if self.__param == "daily":
                counties_data_daily = self.__daily(self.__countries_data)
                for country in self.__countries_list:
                    graph.plot(counties_data_daily[country], label=country)

                graph.set_xlabel("Days (subsequent data)")
                graph.set_ylabel(f"Daily number of {self.__patients_or_cured}")
                graph.grid()
                graph.legend(loc="best")

            elif self.__param == "total":
                for country in self.__countries_list:
                    graph.semilogy(self.__countries_data[country], label=country)

                graph.set_xlabel("Days (subsequent data)")
                graph.set_ylabel(f"Total number of {self.__patients_or_cured}")
                graph.grid()
                graph.legend(loc="best")
        else:
            graph.plot()
            graph.set_xlabel("Days (subsequent data)")
            graph.set_ylabel("Total number of patients")
            graph.grid()

    def __daily(self, countries_data):
        daily = dict()
        for key in countries_data.keys():
            daily[key] = self.__lista_roznic(countries_data[key])
        return daily

    def __lista_roznic(self, lista):
        listab = list()
        for i in range(len(lista)):
            if i == 0:
                listab.append(0)
            else:
                listab.append(lista[i] - lista[i - 1])
        return listab
