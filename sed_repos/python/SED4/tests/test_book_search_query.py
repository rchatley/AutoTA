import unittest
from unittest.mock import Mock
from src.book_search_query_builder import BookSearchQueryBuilder
from src.book import Book


class TestBookSearchQuery(unittest.TestCase):
    def setUp(self):
        self.catalogue = Mock()
        self.builder = BookSearchQueryBuilder(self.catalogue)

    def test_searches_for_books_in_library_catalogue_by_author_surname(self):
        self.catalogue.search_for.return_value = []
        self.builder.with_last_name("dickens").build().execute()
        self.catalogue.search_for.assert_called_once_with("LASTNAME='dickens'")

    def test_searches_for_books_in_library_catalogue_by_author_firstname(self):
        self.catalogue.search_for.return_value = [
            Book("Pride and Prejudice", "Jane Austen", 1813),
            Book("Pride and Prejudice", "Jane Austen", 1813)]
        books = self.builder.with_first_name("Jane").build().execute()
        self.catalogue.search_for.assert_called_once_with("FIRSTNAME='Jane'")
        self.assertEqual(len(books), 2)
        self.assertTrue(books[0].matches_author("Austen"))

    def test_searches_for_books_in_library_catalogue_by_title(self):
        self.catalogue.search_for.return_value = []
        self.builder.containing_title("Two Cities").build().execute()
        self.catalogue.search_for.assert_called_once_with(
            "TITLECONTAINS(Two Cities)")


if __name__ == '__main__':
    unittest.main()
