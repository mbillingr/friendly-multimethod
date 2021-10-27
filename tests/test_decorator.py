from unittest.mock import Mock

from friendly_multimethod import multimethod
from friendly_multimethod.multimethod import MultiMethod


def test_decorating_a_function_creates_a_multimethod():
    @multimethod
    def func():
        return "OK"

    assert isinstance(func, MultiMethod)


def test_decorated_function_is_handler():
    called = False

    @multimethod
    def func():
        nonlocal called
        called = True

    func()

    assert called


def test_decorate_multiple_handlers_calls_last_matching_handler():
    handlers = [Mock(), Mock(), Mock()]

    @multimethod
    def func(x: str):
        handlers[0](x)

    @multimethod
    def func(x: str):
        handlers[1](x)

    @multimethod
    def func(x: int):
        handlers[2](x)

    func("bar")
    handlers[0].assert_not_called()
    handlers[1].assert_called_with("bar")
    handlers[2].assert_not_called()
