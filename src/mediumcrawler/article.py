class MediumArticle:
    def __init__(self, title, link, likes):
        self.title = title
        self.link = link
        self.likes = likes

    def __eq__(self, other): #for sorting out duplicates, 2 articles are considered identical if the title is the same
        return hash(self.title)==hash(other.title)

    def __hash__(self): #for sorting out duplicates, 2 articles are considered identical if the title is the same
        return hash(self.title)