class MediumArticle:
    def __init__(self, title, titlelink, author, authorlink, likes, tags):
        self.title = title
        self.titlelink = titlelink
        self.author = author
        self.authorlink = authorlink
        self.likes = likes
        self.tags = [tags]

    def __eq__(self, other): #for sorting out duplicates, 2 articles are considered identical if the title is the same
        return hash(self.title)==hash(other.title)

    def __hash__(self): #for sorting out duplicates, 2 articles are considered identical if the title is the same
        return hash(self.title)

    def addTag(self, tag):
        self.tags.append(tag)

    def checkKeywords(self, keywords, fields):
        for field in fields:
            if not field in ["title", "author", "tags"]:
                raise ValueError("Field " + field + " not defined within article")

        articleRelated = False
        if "title" in fields:
            if any(keyword.lower() in self.title.lower() for keyword in keywords):
                articleRelated = True
                return articleRelated
        if "author" in fields:
            if any(keyword.lower() in self.author.lower() for keyword in keywords):
                articleRelated = True
                return articleRelated
        if "tags" in fields:
            for tag in self.tags:
                if any(keyword.lower() in tag.lower() for keyword in keywords):
                    articleRelated = True
                    return articleRelated

        return articleRelated

    def __repr__(self) -> str:
        return "MediumArticle('{}','{}','{}','{}','{}','{}')".format(self.title, self.titlelink, self.author, self.authorlink, self.likes, self.tags)