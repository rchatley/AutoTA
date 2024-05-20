from src.book import Book
from src.catalogues.catalogue import Catalogue
from src.catalogues.query_parser import *


class BritishLibraryCatalogue(Catalogue):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BritishLibraryCatalogue, cls).__new__(cls)
            cls._instance.catalogue = cls._instance._all_the_books()
        return cls._instance

    def search_for(self, query):
        return [book for book in self.catalogue
                if book.matches_author(last_name_from(query))
                if book.matches_author(first_name_from(query))
                if book.matches_title(title_from(query))
                if book.published_since(published_after_from(query))
                if book.published_before(published_before_from(query))]

    def _all_the_books(self):
        print("Memory Usage: 500MB...")
        return [
            Book("A Tale of Two Cities", "Charles Dickens", 1859),
            Book("Pride and Prejudice", "Jane Austen", 1813),
            Book("Pride and Prejudice", "Jane Austen", 1813),
            Book("The Picture of Dorian Gray", "Oscar Wilde", 1890),
            Book("Oliver Twist", "Charles Dickens", 1838),
            Book("Frankenstein", "Mary Shelley", 1817),
            Book("Brave New World", "Aldous Huxley", 1932),
            Book("Lord of the Flies", "William Golding", 1954),
            Book("Hamlet", "William Shakespeare", 1603),
            Book("The Life and Opinions of Tristram Shandy, Gentleman",
                 "Laurence Sterne", 1759)
        ]
