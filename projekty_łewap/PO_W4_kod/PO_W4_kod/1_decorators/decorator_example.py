from timeit import default_timer as timer

from _distutils_hack import add_shim


def start_decor(func_to_decor):
    def wrapper(*args, **kwargs):
        print("Starting function...")
        print("Before")
        return func_to_decor(*args, **kwargs)

    return wrapper


def end_decor(func_to_decor):
    def wrapper(*args, **kwargs):
        result = func_to_decor(*args, **kwargs)
        print("After")
        print("Finished!")
        return result

    return wrapper


@start_decor
@end_decor
def add(a=1, b=2):
    print("During")
    return a + b


################
################
################
def measure_time(func_to_measure):
    def wrapper(*args, **kwargs):
        start = timer()
        result = func_to_measure(*args, **kwargs)
        end = timer()
        print("Execution time: {}".format(end - start))
        return result

    return wrapper


@measure_time
def multiply(a, b):
    return a * b


if __name__ == "__main__":
    add_result = add()
    print(add_result)
    mult_result = multiply(2, 8)
    # mult_result = (measure_time(multiply))(10, 2)
    print(mult_result)
