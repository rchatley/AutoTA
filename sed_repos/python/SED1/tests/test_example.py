import unittest
from src.example import Example


class TestExample(unittest.TestCase):
    def test_can_answer_the_universal_question(self):
        example = Example()
        self.assertEqual(example.answer(), 42)


if __name__ == '__main__':
    unittest.main()
