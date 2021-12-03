import colorama as clm
import sympy as sympy
from sympy import *
import numpy as numpy
import matplotlib.pyplot as plt
import control.matlab as mtb
import math


# Функция для получения W(p)
def get_tf(inf, name):
    num = inf.get(name)[0]
    den = inf.get(name)[1]
    return mtb.tf(num, den)

# Функция для построения переходной характеристики
def step(tf):
    print("h(t):\n")
    print(tf)
    [y, x] = mtb.step(tf)
    plt.plot(x, y, "Green")
    plt.title("h(t)")
    plt.xlabel("Time, sec")
    plt.ylabel("Value")
    plt.grid()
    plt.show()

# Функция для вывода на экран полюсов W(p)
def polesWp():
    choice = True
    while choice:
        print(clm.Style.RESET_ALL)
        choice = False
        print("Полюса W(p):\n %s" % mtb.pole(Wzam))
        string = input("\nВведите "1", если полюса левые, введите "2", если - нет:\n")
        if string.isdigit():
            string = int(string)
            if string == 1:
                print("Полюса левые - система устойчива.\n")
            elif string == 2:
                print("Полюса не являются левыми - система неустойчива.\n")
            else:
                print(clm.Fore.CYAN + "\nНекорректное значение!")
                choice = True
        else:
            print(clm.Fore.CYAN + "\nНекорректное значение!")
            choice = True

# Функция для построения годографа Найквиста
def nyquist():
    plt.title("Годограф Найквиста")
    plt.xlabel("Re")
    plt.ylabel("Im")
    mtb.nyquist(Wraz)
    plt.grid(True)
    plt.plot()
    plt.show()

# Функция для построения ЛАЧХ и ЛФЧХ
def fCh():
    print("ЛАЧХ и ЛФЧХ изображены на графике.\n")
    mtb.bode(Wraz, dB=False)
    plt.plot()
    plt.xlabel("Частота (Гц)")
    plt.show()

# Построение годографа Михайлова
def mikh():
    a, p = symbols("a, p")
    a_list = mtb.tfdata(Wzam)[1][0][0]
    w = numpy.arange(0, 2.0, 0.05)
    expr = sum([a_list[i] * p ** (len(a_list) - i - 1) for i in range(len(a_list))])
    print("Уравнение: ", end="")
    print(expr)
    val = list(map(lambda x: expr.subs(p, complex(0, x)), w))
    u, v = list(map(re, value)), list(map(im, val))
    plt.plot(u, v)
    plt.title("Годограф Михайлова")
    plt.xlabel("Re")
    plt.ylabel("Im")
    plt.grid()
    plt.show()
