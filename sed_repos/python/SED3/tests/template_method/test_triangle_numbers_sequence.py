import unittest
from src.template_method.triangle_numbers_sequence import \
    TriangleNumbersSequence
from tests.matchers.iterable_begins_with import IterableBeginsWith


class TriangleNumbersSequenceTest(unittest.TestCase):

    def setUp(self):
        self.sequence = TriangleNumbersSequence()

    def test_defines_first_term_to_be_one(self):
        self.assertEqual(self.sequence.term(0), 1)

    def test_defines_subsequent_terms_to_be_half_of_the_product_of_next_two_indices(
            self):
        self.assertEqual(self.sequence.term(1), 3)
        self.assertEqual(self.sequence.term(2), 6)
        self.assertEqual(self.sequence.term(3), 10)

    def test_is_undefined_for_negative_indices(self):
        with self.assertRaises(ValueError):
            self.sequence.term(-1)

    def test_can_be_iterated_through(self):
        self.assertTrue(
            IterableBeginsWith(1, 3, 6, 10, 15).matches(self.sequence))


if __name__ == '__main__':
    unittest.main()
