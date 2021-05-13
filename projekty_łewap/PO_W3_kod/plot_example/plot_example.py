import numpy as np
from math import pi, sin, cos
from matplotlib import pyplot as plt

n = 100

X = np.linspace(0, 2*pi, n)
Y_sin = [sin(x_val) for x_val in X]
Y_cos = [cos(x_val) for x_val in X]

plt.subplot2grid((2, 2), (0, 0))
plt.plot(X, Y_sin, "-r")
plt.xlabel("x")
plt.ylabel("sin(x)")
plt.xlim([0, 2*pi])
plt.title("Wykres sin(x)")

plt.subplot2grid((2, 2), (1, 0))
plt.plot(X, Y_cos, "-b")
plt.xlabel("x")
plt.ylabel("cos(x)")
plt.title("Wykres cos(x)")

plt.subplot2grid((2, 2), (0, 1), rowspan=2)
plt.plot(X, Y_sin, "-g", label="sin(x)")
plt.plot(X, Y_cos, "-k", label="cos(x)")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend(loc="best")
plt.title("Wykresy funkcji: sin(x), cos(x)")

plt.tight_layout()

plt.show()
