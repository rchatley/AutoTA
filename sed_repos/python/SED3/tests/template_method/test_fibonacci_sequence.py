import unittest
from src.template_method.fibonacci_sequence import FibonacciSequence
from tests.matchers.iterable_begins_with import IterableBeginsWith


class FibonacciSequenceTest(unittest.TestCase):

    def setUp(self):
        self.sequence = FibonacciSequence()

    def test_defines_first_two_terms_to_be_one(self):
        self.assertEqual(self.sequence.term(0), 1)
        self.assertEqual(self.sequence.term(1), 1)

    def test_defines_subsequent_terms_to_be_the_sum_of_the_previous_two(self):
        self.assertEqual(self.sequence.term(2), 2)
        self.assertEqual(self.sequence.term(3), 3)
        self.assertEqual(self.sequence.term(4), 5)

    def test_is_undefined_for_negative_indices(self):
        with self.assertRaises(ValueError):
            self.sequence.term(-1)

    def test_can_be_iterated_through(self):
        self.assertTrue(
            IterableBeginsWith(1, 1, 2, 3, 5).matches(self.sequence))


if __name__ == '__main__':
    unittest.main()
