#!/usr/bin/env python3

"""A comparison between python standard library and numpy performance.
In the first case a list of random numbers is generated and sorted.
In the second case an array of random numbers is generated and sorted """
import numpy as np
from random import random
import cProfile


def main():
    cProfile.run('list_tester()')
    cProfile.run('array_tester()')


def list_tester():
    """Creates a list of random numbers, and sorts it"""
    list_container = [random() for i in range(0, 1000000)]
    list_container = sorted(list_container)
    return list_container


def array_tester():
    """Creates an array of random numbers and sorts it"""
    array_container = np.random.rand(1000000)
    array_container = np.sort(array_container)
    return array_container


if __name__ == '__main__':
    main()
