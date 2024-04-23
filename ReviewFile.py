from javalang import parse, tokenizer


class ReviewFile:

    def __init__(self, root, file_name, contents):
        self.root = root
        self.file_name = file_name
        self.contents = contents
        self.tokens = list(tokenizer.tokenize(contents))
        self.ast = parse.parse(contents)
