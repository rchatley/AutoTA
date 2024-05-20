from src.strategy.term_generator import TermGenerator
from typing import Iterator


class Sequence:
    def __init__(self, term_generator: TermGenerator):
        self.term_generator = term_generator

    def term(self, i: int) -> int:
        if i < 0:
            raise ValueError("Not defined for indices < 0")
        return self.term_generator.term(i)

    def __iter__(self) -> Iterator[int]:
        return self.SequenceIterator(self)

    class SequenceIterator:
        def __init__(self, sequence):
            self.sequence = sequence
            self.index = 0

        def __iter__(self):
            return self

        def __next__(self) -> int:
            result = self.sequence.term(self.index)
            self.index += 1
            return result
