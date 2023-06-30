#!/usr/bin/env python3

""" Compares the performance of creating lists """

import inspect
from time import time


def tester(fun, n):
    """ Measures the time to run the list creation function for n elements """
    start = time()
    fun(n)
    print(f"{inspect.getsource(fun)}{time() - start} sec\n")


def main(n):
    tester(list_comprehension, n)
    tester(list_append, n)
    tester(list_initialisation, n)


def list_comprehension(n):
    return [i for i in range(0, n)]


def list_append(n):
    lst = []
    for i in range(0, n):
        lst.append(i)
    return lst


def list_initialisation(n):
    lst = [0] * n
    for i in range(0, n):
        lst[i] = i
    return lst


if __name__ == '__main__':
    main(100000000)
