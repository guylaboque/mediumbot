class MediumArticle:
    def __init__(self, title, titlelink, author, authorlink, likes):
        self.title = title
        self.titlelink = titlelink
        self.author = author
        self.authorlink = authorlink
        self.likes = likes

    def __eq__(self, other): #for sorting out duplicates, 2 articles are considered identical if the title is the same
        return hash(self.title)==hash(other.title)

    def __hash__(self): #for sorting out duplicates, 2 articles are considered identical if the title is the same
        return hash(self.title)
