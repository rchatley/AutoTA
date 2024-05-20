from typing import Iterator


class Sequence:
    def term(self, i: int) -> int:
        if i < 0:
            raise ValueError("Not defined for indices < 0")
        return self.generate_term(i)

    def generate_term(self, i: int) -> int:
        raise NotImplementedError("generate_term method not implemented")

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
