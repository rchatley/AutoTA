from src.book_search_query import BookSearchQuery


class BookSearchQueryBuilder:
    def __init__(self, catalogue):
        self.first_name = None
        self.last_name = None
        self.title = None
        self.published_after_date = None
        self.published_before_date = None
        self.catalogue = catalogue

    def build(self):
        return BookSearchQuery(self.first_name, self.last_name, self.title,
                               self.published_after_date,
                               self.published_before_date, self.catalogue)

    def with_first_name(self, first_name):
        self.first_name = first_name
        return self

    def with_last_name(self, last_name):
        self.last_name = last_name
        return self

    def containing_title(self, title):
        self.title = title
        return self

    def published_after(self, min_publication_date):
        self.published_after_date = min_publication_date
        return self

    def published_before(self, max_publication_date):
        self.published_before_date = max_publication_date
        return self
