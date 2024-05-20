class BookSearchQuery:
    def __init__(self, name1, name2, title, date1, date2, catalogue):
        self.name1 = name1
        self.name2 = name2
        self.title = title
        self.date1 = date1
        self.date2 = date2
        self.catalogue = catalogue

    def execute(self):
        query = []
        if self.name1:
            query.append(f"FIRSTNAME='{self.name1}'")
        if self.name2:
            query.append(f"LASTNAME='{self.name2}'")
        if self.title:
            query.append(f"TITLECONTAINS({self.title})")
        if self.date1:
            query.append(f"PUBLISHEDAFTER({self.date1})")
        if self.date2:
            query.append(f"PUBLISHEDBEFORE({self.date2})")
        query_str = " ".join(query)

        return self.catalogue.search_for(query_str)
