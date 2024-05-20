from src.strategy.term_generator import TermGenerator


class TriangleNumbersGenerator(TermGenerator):
    def term(self, i: int) -> int:
        if i == 0:
            return 1
        return (i + 1) * (i + 2) // 2
