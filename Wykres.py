from io import BytesIO

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator


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
        graph.set_xlabel("Days (subsequent data)")
        graph.set_ylabel(f"{self.__param.capitalize()} number of {self.__patients_or_cured}")
        graph.grid()
        if self.__countries_data and self.__countries_list:
            ile_miesiecy = len(self.__countries_data["Poland"])/30
            odstep_miedzy_punktami_x = len(self.__countries_data["Poland"])/ile_miesiecy  # to powinno być (max - min)/12 (wartosci ze sliderów)
            graph.xaxis.set_major_locator(MultipleLocator(odstep_miedzy_punktami_x))
            x = self.__countries_data["Country/Region"]
            graph.tick_params(axis ='x', rotation = 45)
            if self.__param == "daily":
                countries_data_daily = self.__daily(self.__countries_data)
                for country in self.__countries_list:
                    graph.plot(x, countries_data_daily[country], label=country)
                graph.legend(loc="best")

            elif self.__param == "total":
                for country in self.__countries_list:
                    graph.semilogy(x, self.__countries_data[country], label=country)
                graph.legend(loc="best")
        else:
            graph.plot()

    def __daily(self, countries_data):
        daily = dict()
        keys = list(countries_data.keys())[1:]
        for key in keys:
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
