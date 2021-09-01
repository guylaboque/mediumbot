from typing import DefaultDict


class Category:
    def __init__(self, name, keywords, order=0, articles = None, default = False, tgId=None,):
        self.name = name
        self.keywords = keywords
        self.tgId = tgId
        self.order = order
        if articles is None:
            self.articles = []
        else:
            self.articles = articles
        self.default = default

    def addArticle(self, article):
        self.articles.append(article)
        self.articles.sort(key= lambda article: int(article.likes), reverse=True) #sort by likes


    def __repr__(self) -> str:
        articlenames = []
        for article in self.articles:
            articlenames.append(article.title)

        return "Category('{}', '{}', '{}', '{}', '{}', '{}')".format(self.name, self.keywords, self.tgId, self.order, articlenames, self.default)