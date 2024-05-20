class Book:
    def __init__(self, title, author, published):
        self.title = title
        self.author = author
        self.published = published

    def matches_author(self, author):
        return author is None or (author.lower() in self.author.lower())

    def published_before(self, year):
        return year is None or (self.published < year)

    def published_since(self, year):
        return year is None or (self.published > year)

    def matches_title(self, title):
        return title is None or (title.lower() in self.title.lower())

    def __str__(self):
        return f"{self.title}, by {self.author}, published {self.published}"
