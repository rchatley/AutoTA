import unittest

from sample_repos.python.SED1.src.main.Example import Example


class ExampleTest(unittest.TestCase):
    def test_can_answer_the_universal_question(self):
        self.assertEqual(Example().answer(), 42)


if __name__ == '__main__':
    unittest.main()
