from src.strategy.term_generator import TermGenerator


class FibonacciGenerator(TermGenerator):
    def term(self, i: int) -> int:
        if i < 2:
            return 1
        return self.term(i - 1) + self.term(i - 2)
