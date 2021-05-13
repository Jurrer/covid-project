from dunder_method.name import Name


def main():
    name_1 = Name("Hans")
    name_2 = Name("Pinokio")

    print(name_1)
    print(name_1.name)
    result = name_1 + name_2
    print(4 + 6)
    print(result)


if __name__ == "__main__":
    main()
