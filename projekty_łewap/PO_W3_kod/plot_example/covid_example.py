# data from: https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases
import sys

from matplotlib import pyplot as plt

COUNTRY_COLUMN_ID = 1


def display_selected_data(filepath, countries):
    countries_data = read_countries_data(filepath, countries)
    display_data(countries_data)


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


def get_patients_as_vector(country_data_line):
    n_of_unimportant_column = 4
    n_of_patients_in_time = country_data_line.split(",")[n_of_unimportant_column:]
    n_of_patients_in_time = [int(val) for val in n_of_patients_in_time]

    return n_of_patients_in_time


def display_data(n_of_patients_in_countries):
    for country, data in n_of_patients_in_countries.items():
        plt.semilogy(data, label=country)

    plt.xlabel("Days (subsequent data)")
    plt.ylabel("Total number of patients")
    plt.title("Covid-19 number of patients since 01.01.2020")
    plt.grid()
    plt.legend()
    plt.show()


def validate_args(args):
    if len(args) < 2:
        print("Incorrect arguments. Expected filename and list of countries", file=sys.stderr)
        exit(-1)


if __name__ == "__main__":
    args = sys.argv
    validate_args(args)

    filepath = args[1]
    country_names = args[2].split(",")

    display_selected_data(filepath, country_names)
