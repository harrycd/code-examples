#!/usr/bin/env python

"""Example of using deque in a fibonacci series generator"""

from collections import deque
import time


def fibonacci_generator():
    """
    Generates fibonacci series numbers using deque

    :return: the [next] fibonacci number
    :rtype: int
    """
    last_two_n = deque([0, 1])

    yield 0
    yield 1

    while True:
        s = sum(last_two_n)
        yield s
        last_two_n.append(s)
        last_two_n.popleft()


def fibonacci_generator_optimum():
    """
    Generates fibonacci series numbers the optimum way.

    :return: the [next] fibonacci number
    :rtype: int
    """
    yield 0
    yield 1

    f, fn = 0, 1
    while True:
        yield f
        f, fn = fn, f + fn


def generator_tester(gen, iterations=1000):
    """
    Measures the performance of a generator and prints the results

    :param gen: the generator whose performance is measured
    :type gen: generator
    :param iterations: how many times will the generator be called
    :type iterations: int
    """
    start_time = 0
    end_time = 0
    it = 0
    start_time = time.time()
    while it < iterations:
        next(gen)
        it += 1

    end_time = time.time()

    print(f"generator run time: {end_time - start_time}")


generator_tester(fibonacci_generator(), 100000)
generator_tester(fibonacci_generator_optimum(), 100000)


# print some numbers for fun
print("\n\nLets print some numbers in memory of filius Bonacci")

stop_after = 10
for i, n in enumerate(fibonacci_generator()):
    if i > stop_after-2:
        print(n)
        break
    print(n, end=', ')
