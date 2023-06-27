#!/usr/bin/env python3

"""A comparison of different ways to calculate an integer number's square"""
import math

import numpy as np
from time import time
from math import pow


def tester(fun):
    """Measures the time to run the function 10000000 times"""
    start = time()
    for i in range(0, 10000000):
        fun(i)
    print(time() - start)


def main():
    tester(fun=lambda i: i ** 2)
    tester(fun=lambda i: math.pow(i, 2))
    tester(fun=lambda i: pow(i, 2))
    tester(fun=lambda i: i * i)
    tester(fun=lambda i: np.power(i, 2))


if __name__ == '__main__':
    main()
