#!/usr/bin/env python3

"""A comparison of different ways to calculate a number's square"""
import numpy as np
from time import time


def tester(fun):
    """Measures the time to run the function 10000000 times"""
    start = time()
    for i in range(0, 10000000):
        fun(i)
    print(time() - start)


def main():
    tester(fun=lambda i: i ** 2)
    tester(fun=lambda i: pow(i, 2))
    tester(fun=lambda i: i * i)
    tester(fun=lambda i: np.power(i, 2))


if __name__ == '__main__':
    main()
