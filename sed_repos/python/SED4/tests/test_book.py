import unittest
from src.book import Book


class TestBook(unittest.TestCase):
    def setUp(self):
        self.oliver_twist = Book("Oliver Twist", "Charles Dickens", 1859)

    def test_supports_case_insensitive_author_query(self):
        self.assertTrue(self.oliver_twist.matches_author("Dickens"))
        self.assertTrue(self.oliver_twist.matches_author("dickens"))
        self.assertTrue(self.oliver_twist.matches_author("charles"))
        self.assertFalse(self.oliver_twist.matches_author("Shakespeare"))
        self.assertTrue(self.oliver_twist.matches_author(None))

    def test_supports_case_insensitive_title_query(self):
        self.assertTrue(self.oliver_twist.matches_title("Twist"))
        self.assertTrue(self.oliver_twist.matches_title("twist"))
        self.assertFalse(self.oliver_twist.matches_title("Cities"))
        self.assertTrue(self.oliver_twist.matches_title(None))

    def test_supports_publication_date_query(self):
        self.assertTrue(self.oliver_twist.published_before(1900))
        self.assertTrue(self.oliver_twist.published_since(1800))
        self.assertFalse(self.oliver_twist.published_before(1800))
        self.assertFalse(self.oliver_twist.published_since(1900))

    def test_converts_to_formatted_string_of_title_and_author(self):
        self.assertEqual(str(self.oliver_twist),
                         "Oliver Twist, by Charles Dickens, published 1859")


if __name__ == '__main__':
    unittest.main()
