from src.template_method.sequence import Sequence


class TriangleNumbersSequence(Sequence):
    def generate_term(self, i: int) -> int:
        if i == 0:
            return 1
        return (i + 1) * (i + 2) // 2
