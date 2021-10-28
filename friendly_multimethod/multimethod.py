import itertools as it
from inspect import signature
from typing import Callable, List, Optional


class MultiMethod:
    def __init__(self, handlers: Optional[List[Callable]] = None):
        self.handlers = handlers or []
        for h in self.handlers:
            normalize_annotations(h)

    def __call__(self, *args, **kwargs):
        for h in self.handlers[::-1]:
            if check_args(h, args, kwargs):
                return h(*args, **kwargs)

        call_sig = build_call_signature_str(args, kwargs)
        raise TypeError(f"No handler for call ({call_sig})")

    def add_handler(self, handler: Callable):
        normalize_annotations(handler)
        self.handlers.append(handler)


def check_args(func, args, kwargs):
    """Test if arguments match function's annotated signature"""
    sig = signature(func)
    try:
        bound_args = sig.bind(*args, **kwargs)
    except TypeError:
        return False

    for name, value in bound_args.arguments.items():
        ann = func.__annotations__.get(name)
        if ann and not ann(value):
            return False
    return True


def build_call_signature_str(args, kwargs):
    arg_strings = (str(a) for a in args)
    kwarg_strings = (f"{k}={repr(v)}" for k, v in kwargs.items())
    call_sig = ", ".join(it.chain(arg_strings, kwarg_strings))
    return call_sig


def normalize_annotations(func: Callable):
    """Convert all annotations to predicate functions"""
    new_annotations = {}
    for name, ann in getattr(func, "__annotations__", {}).items():
        if isinstance(ann, type):
            new_annotations[name] = lambda obj, t=ann: isinstance(obj, t)
        else:
            new_annotations[name] = ann
    func.__annotations__ = new_annotations
