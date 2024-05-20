from typing import Iterable, TypeVar
import unittest

T = TypeVar('T')


class IterableBeginsWith(unittest.TestCase):
    def __init__(self, *elems: T):
        super().__init__()
        self.target = list(elems)

    def matches(self, iterable: Iterable[T]) -> bool:
        iterator = iter(iterable)
        for i, expected in enumerate(self.target):
            try:
                value = next(iterator)
            except StopIteration:
                self.fail(
                    f"Not enough items, expected {expected} at position {i}")
            if value != expected:
                self.fail(
                    f"Found {value} instead of {expected} at position {i}")
        return True
