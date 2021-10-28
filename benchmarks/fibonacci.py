from timeit import timeit, repeat

from friendly_multimethod import multimethod


def less_than(n):
    return lambda x: x < n


@multimethod
def fib(n: int):
    return fib(n-1) + fib(n-2)


@multimethod
def fib(_: less_than(2)):
    return 1

print(fib(5))

print(repeat("fib(10)", number=100, globals=globals()))
