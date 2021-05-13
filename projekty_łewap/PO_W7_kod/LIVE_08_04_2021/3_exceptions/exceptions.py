class A(Exception):
    pass


class B(A):
    pass


class C(B):
    pass


exceptions = [A, B, C]

for exception in exceptions:
    try:
        raise exception
        # pass
    # Ważna jest hierarchia
    except A:
        print("Caught A")
    except B:
        print("Caught B")
    except C:
        print("Caught C")
    finally:
        print("Finished work")
