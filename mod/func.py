"""
func.py

This module provides static functions.

Main functions:
- timed(func)


Exceptions:
-

Examples of using:

>>> from mod.func import timed
>>> @timed

"""
from functools import wraps
from time import perf_counter


def timed(func):
    """
    (rus) Функция декоратор, которая при вызове декорируемой функции измеряет время ее выполнения \n
    (eng) Decorator function, which, when calling the decorated function, measures its execution time

    """
    @wraps(func)
    def wrap(*args, **kwargs):
        t1 = perf_counter()
        result = func(*args, **kwargs)
        t2 = perf_counter()
        print(f"Calling {func.__name__} took {t2-t1} second, ", end="")
        print(f"(with parameters {args}, {kwargs})")
        return result
    return wrap
