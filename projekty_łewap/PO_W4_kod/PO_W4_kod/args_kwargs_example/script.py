def f(a, b, *args, **kwargs):
    print("Sum a+b: {}".format(a + b))

    kwargs_sum = sum(kwargs.values())
    print("Sum kwargs: {}".format(kwargs_sum))

    print("Sum args: {}".format(sum(args)))


nums = [5, 2, 3, 10]
f(5, 3, 4, d=6, e=4)
