from src.template_method.sequence import Sequence


class FibonacciSequence(Sequence):
    def generate_term(self, i: int) -> int:
        if i < 2:
            return 1
        return self.generate_term(i - 1) + self.generate_term(i - 2)
