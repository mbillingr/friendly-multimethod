from unittest.mock import Mock

import pytest

from friendly_multimethod.multimethod import MultiMethod


def test_multimethods_are_callable():
    method = MultiMethod()
    assert callable(method)


def test_calling_an_empty_multimethod_fails():
    method = MultiMethod()
    with pytest.raises(TypeError):
        method()


def test_add_handler_to_multimethod():
    method = MultiMethod()
    method.add_handler(lambda: 0)
    method()  # does not raise


def test_multimethod_returns_result_from_handler():
    result = Mock()
    method = MultiMethod(handlers=[lambda: result])
    assert method() is result


def test_multimethod_passes_args_to_handler():
    handler = Mock()
    method = MultiMethod(handlers=[lambda *args, **kwargs: handler(*args, **kwargs)])
    method(1, 2, z=3)
    handler.assert_called_once_with(1, 2, z=3)


def test_calling_multimethod_with_unmatched_types_fails():
    def handler(x: int) -> int:
        return x

    method = MultiMethod(handlers=[handler])
    with pytest.raises(TypeError):
        method("foo")


def test_calling_multimethod_last_added_handlers_take_precedence():
    handlers = [Mock(), Mock()]
    method = MultiMethod(handlers=handlers)
    method()

    handlers[0].assert_not_called()
    handlers[1].assert_called_once()


def test_multimethod_finds_handler_even_if_more_generic_parameter_fails():
    def handler1(a: int, b: str):
        called.add(handler1)

    def handler2(a, b: int):
        called.add(handler2)

    called = set()

    method = MultiMethod(handlers=[handler1, handler2])

    # this call signature matches only the first argument of handler2 but not the second
    method(1, "x")

    # the multimethod should call handler1 although the first argument on handler2 is more generic
    assert handler1 in called
    assert handler2 not in called


def test_multimethod_tries_next_handler_if_binding_fails():
    def handler1():
        called.add(handler1)

    def handler2(x):
        called.add(handler2)

    called = set()

    method = MultiMethod(handlers=[handler1, handler2])

    # this call signature matches only the first argument of handler2 but not the second
    method()

    # the multimethod should call handler1 although the first argument on handler2 is more generic
    assert handler1 in called
    assert handler2 not in called


def test_dispatch_on_predicate():
    def even(x: lambda x: x % 2 == 0):
        return "even"

    def odd(x: lambda x: x % 2 == 1):
        return "odd"

    method = MultiMethod(handlers=[even, odd])

    assert method(42) == "even"
