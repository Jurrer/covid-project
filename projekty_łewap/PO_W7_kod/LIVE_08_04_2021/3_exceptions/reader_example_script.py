def read_from_file(filename):
    try:
        with open(filename, "r") as f:
            for line in f:
                print(line)
    except Exception as err:
        print("Cannot read from file (filename: {}). File not found!".format(filename))
    except FileNotFoundError as err:
        pass



read_from_file("plik_nie_istnieje.txt")
# read_from_file("dane.txt")
print("Działam dalej")
