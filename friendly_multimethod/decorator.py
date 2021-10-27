from typing import Callable
from weakref import WeakValueDictionary

from friendly_multimethod.multimethod import MultiMethod

KNOWN_MULTIMETHODS = WeakValueDictionary()


def multimethod(func: Callable) -> Callable:
    """Multimethod Decorator.

    Define a new multimethod with

    >>> @multimethod
    ... def foo(*__, **_):
    ...     print('hello, default handler!')

    Similarly, add more handlers

    >>> @multimethod
    ... def foo(x: int):
    ...     print(f'hello, {x}-valued integer!')

    >>> foo(42)
    hello, 42-valued integer!
    >>> foo('bar')
    hello, default handler!
    """
    func_name = get_fully_qualified_name(func)
    try:
        method = KNOWN_MULTIMETHODS[func_name]
    except KeyError:
        method = MultiMethod()
        KNOWN_MULTIMETHODS[func_name] = method
    method.add_handler(func)
    return method


def get_fully_qualified_name(obj):
    return f"{obj.__module__}.{obj.__qualname__}"
