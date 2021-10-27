import itertools as it
from inspect import signature
from typing import Callable, List, Optional


class MultiMethod:
    def __init__(self, handlers: Optional[List[Callable]] = None):
        self.handlers = handlers or []

    def __call__(self, *args, **kwargs):
        for h in self.handlers[::-1]:
            if check_args(h, args, kwargs):
                return h(*args, **kwargs)
        call_sig = build_call_signature_str(args, kwargs)
        raise TypeError(f"No handler for call ({call_sig})")

    def add_handler(self, handler: Callable):
        self.handlers.append(handler)


def check_args(func, args, kwargs):
    sig = signature(func)
    bound_args = sig.bind(*args, **kwargs)
    annotations = getattr(func, "__annotations__", {})
    for name, value in bound_args.arguments.items():
        if not isinstance(value, annotations.get(name, object)):
            return False
    return True


def build_call_signature_str(args, kwargs):
    arg_strings = (str(a) for a in args)
    kwarg_strings = (f"{k}={v}" for k, v in kwargs)
    call_sig = ", ".join(it.chain(arg_strings, kwarg_strings))
    return call_sig
