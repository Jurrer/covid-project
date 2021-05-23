import matplotlib as plt
class Wykres:
    def __init__(self, countries_data):
        self.__countries_data = countries_data

    def display_data(self, counties_data):
        for country, data in counties_data.items():
            plt.semilogy(data, label=country)

        plt.xlabel("Days (subsequent data)")
        plt.ylabel("Total number of patients")
        # plt.title("Covid-19 number of patients since 01.01.2020")
        plt.grid()
        plt.legend(loc="lower right")
        plt.tight_layout()
        plt.show()
