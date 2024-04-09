from javalang import parse


class ReviewFile:

    def __init__(self, name, contents):
        self.name = name
        self.contents = contents
        self.ast = parse.parse(contents)
