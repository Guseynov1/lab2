import colorama as clm
import control
import matplotlib.pyplot
import sympy as sympy
from sympy import *
import numpy as numpy
import matplotlib.pyplot as plt
import control.matlab as mtb
import math
from numpy import arange

Koc = 8
# Исходные данные
OS = mtb.tf([Koc, 0], [0, 1])
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

# Михайлов
# Просуммируем числитель и знаменатель Wzam
sumnum = [float(x) for x in Wzam.num[0][0]]
sumden = [float(x) for x in Wzam.den[0][0]]
funmikh = []
print(funmikh)
for i in range(len(sumden) - len(sumnum)):
    sumnum.insert(0, 0)
for i in range(len(sumnum)):
    funmikh.append(sumnum[i] + sumden[i])
print(funmikh)
# устойчивость
funmikh = funmikh[::-1]
j = sympy.I
om = sympy.symbols("w")
for i in range(len(funmikh)):
    funmikh[i] = funmikh[i] * (j * om) ** i
x = numpy.arange(0, 1, 0.01)
mc = []
for i in x:
    sum = 0
    for k in funmikh:
        sum += k.subs(om, i)
    mc.append(sum)

real = [sympy.re(x) for x in mc]
imaginary = [sympy.im(x) for x in mc]
num = 1
flagcros = False
flagposcrosX = True
flagposcrosY = True
for i in range(len(mc) - 1):
    if ((real[i] >= 0 and real[i + 1] <= 0) or (real[i] <= 0 and real[i + 1] >= 0)):
        if flagposcrosX:
            num += 1
            flagposcrosX = False
            flagposcrosX = True
        if imaginary[i] > 0:
            flagcros = True
    if ((imaginary[i] >= 0 and imaginary[i + 1] <= 0) or (imaginary[i] <= 0 and imaginary[i + 1] >= 0)):
        if flagposcrosY:
            num += 1
            flagposcrosX = True
            flagposcrosX = False
    if num >= 3 and flagcros:
        print("Система устойчива по Михайлову")
    else:
        print("Система устойчива по Михайлову")

plt.title("Михайлов")
ex = matplotlib.pyplot.gca()
ex.plot(real, imaginary)
ex.grid(True)
ex.spines["left"].set_position("zero")
ex.spines["right"].set_color("none")
ex.spines["bottom"].set_position("zero")
ex.spines["top"].set_color("none")
plt.xlim(-250, 250)
plt.ylim(-250, 250)
plt.xlabel("re")
plt.ylabel("im")
plt.show()

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
