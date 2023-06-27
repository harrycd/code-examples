#!/usr/bin/env python3

"""A comparison of different ways to calculate the square root of an integer"""
import math
import inspect
import numpy as np
from time import time
from math import pow


def tester(fun):
    """Measures the time to run the function 10000000 times"""
    start = time()
    for i in range(0, 10000000):
        fun(i)
    print(f"{inspect.getsource(fun)}{time() - start} sec\n")


def main():
    tester(fun=lambda i: i ** 0.5)
    tester(fun=lambda i: math.pow(i, 0.5))
    tester(fun=lambda i: math.sqrt(i))
    tester(fun=lambda i: pow(i, 2))
    tester(fun=lambda i: pow(i, 0.5))
    tester(fun=lambda i: np.power(i, 0.5))
    tester(fun=lambda i: np.sqrt(i))


if __name__ == '__main__':
    main()
