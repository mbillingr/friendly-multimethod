# friendly-multimethod

Multiple dispatch on types and predicates.

## Quickstart

Define a new multimethod with

```python
>>> from friendly_multimethod import multimethod

>>> @multimethod
... def foo(*__, **_):
...     print('hello, default handler!')

```

Similarly, add more handlers

```python
>>> @multimethod
... def foo(x: int):
...     print(f'hello, {x}-valued integer!')

```

```python
>>> foo(42)
hello, 42-valued integer!
>>> foo('bar')
hello, default handler!

```

## Coming Soon

- predicate-based dispatch
- PyPi package
- continuous integration
