import colorama as clm
import control
import sympy as sympy
from sympy import *
import numpy as numpy
import matplotlib.pyplot as plt
import control.matlab as mtb
import math
from numpy import arange


# Исходные данные
OS = mtb.tf([8, 0], [0, 1])
GEN = mtb.tf([1], [7, 1])
GTurb = mtb.tf([0.02, 1], [0.35, 1])
IUstr = mtb.tf([24], [5, 1])
W = GEN * GTurb * IUstr
Wzam = mtb.feedback(W, OS)
Wraz = W

print("W(p) замкнутой системы")
print(Wzam)

# Функция для построения переходной характеристики
[y, x] = mtb.step(Wzam)
plt.plot(x, y)
plt.title("h(t)")
plt.xlabel("time (c)")
plt.ylabel("amplitude")
plt.grid(True)
plt.show()


# Определение полюсов W(p) замкнутой САУ
a = mtb.pole(Wzam)
b = mtb.zero(Wzam)
print("Полюса W(p) замкнутой САУ:\n", a)
print("Нули W(p) замкнутой САУ:\n", b)
stab = True

control.pzmap(Wzam, title="Карта полюсов и нулей Wzam")
plt.show()

print("W(p) разомкнутой системы")
print(Wraz)

for i in mtb.pole(Wzam):
    if i.real > 0:
        stab = False
        break

print("устойчива" if stab else "неустойчива")

# Функция для построения годографа Найквиста
mtb.nyquist(Wraz)
plt.grid(True)
plt.title("Годограф Найквиста")
plt.xlabel("Re")
plt.ylabel("Im")
plt.show()

# Функция для построения ЛАЧХ и ЛФЧХ
mtb.bode(Wraz, omega_limits=[0.01, 1e3])
plt.show()

def fCh():
    print("ЛАЧХ и ЛФЧХ изображены на графике.\n")
    mtb.bode(Wraz, dB=False)
    plt.plot()
    plt.xlabel("Частота (Гц)")
    plt.show()

# Построение годографа Михайлова
    u = mtb.tfdata(Wzam)[1][0][0]
    dicu = {}
    dlinu = len(u)
    for i in range(dlinu):
        dicu["%s" % i] = u[i]
    w = symbols("w", real=True)
    z = -(dicu["0"]) * I * w ** 3 - (dicu["1"]) * w ** 2 + (dicu["2"]) * I * w + (dicu["3"])
    # z = -12.25 * I * w ** 3 - 43.04 * w ** 2 + 204.83 * I * w + 25 для k = 22
    print("Характеристический многочлен замкнутой системы: %s" % z)
    zr = re(z)
    zm = im(z)
    print("Real Re= %s" % zr)
    print("Imagin Im= %s" % zm)
    plt.figure()
    plt.title("Годограф Михайлова")
    x = [zr.subs({w: q}) for q in numpy.arange(0, 100, 0.1)]
    y = [zm.subs({w: q}) for q in numpy.arange(0, 100, 0.1)]
    plt.axis([-100.0, 100.0, -100.0, 100.0])
    plt.plot(x, y)
    plt.grid(True)
    return

# Поиск Кос
for Koc in numpy.arange(0, 100, 0.01):
    OS = mtb.tf([Koc, 0], [0, 1])
    Wzam = mtb.feedback(W, OS)
    c = Wzam.den[0][0]
    cf = {}
    size = len(c)
    for j in range(0, size):
        cf["%s" % j] = c[j]
    matrix = numpy.array([[cf["1"], cf["3"]], [cf["0"], cf["2"]]])
    if (numpy.linalg.det(matrix) >= -0.0001) & (numpy.linalg.det(matrix) <= 0.0001):
        print("Предельное значение коэффициента ОС:", Koc)
        break
