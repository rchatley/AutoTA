class ReviewProject:

    def __init__(self, language, files):
        self.language = language
        self.files = files

    def apply_rules(self, rules):
        if rules is None:
            return

        for file in self.files:
            for rule in rules:
                print(rule.apply(file))
