import requests
import logging
from bs4 import BeautifulSoup

from .article import MediumArticle
from .urls import getTagUrl

def convert_str_to_number(x):
    final_number = 0
    num_map = {'K':1000, 'M':1000000, 'B':1000000000}
    if x.isdigit():
        final_number = int(x)
    else:
        if len(x) > 1:
            final_number = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return int(final_number)

def getArticles(tag, crawlDate):
    url = getTagUrl(tag, crawlDate)
    response = requests.get(url)
    mediumPage = BeautifulSoup(response.text, 'html.parser')

    articleElements = mediumPage.findAll('div', attrs={"class":"postArticle--short"}) #get whole elements for blog posts

    articles = []

    for blogPost in articleElements:

        title_check = blogPost("h3", "graf--title")
        if not title_check: #skip articles without a title
            continue
        title = str(title_check[0].string) #create comparable string of title

        titlelink = blogPost("a", attrs={"data-action": "open-post"})[0].get('href').split("?")[0]

        author = blogPost("a", attrs={"data-action": "show-user-card"})[1].string

        authorlink = blogPost("a", attrs={"data-action": "show-user-card"})[0].get('href').split("?")[0]

        likeData = blogPost("button", attrs={"data-action": "show-recommends"})

        if not likeData:
            likes = "0"
        else:
            likes = str(convert_str_to_number(likeData[0].string))

        article = MediumArticle(title, titlelink, author, authorlink ,likes, tag)
        articles.append(article)

    if len(articles) == 0:
        logging.warning("No articles found, maybe something changed in the page structure")

    return articles

def mergeArticleLists(*articleLists):
    mergedArticleList = []
    for articleList in articleLists:
        for article in articleList: #check for each element of the second list if its already in the first list and if not add it
            if len(mergedArticleList) == 0:
                mergedArticleList.append(article)
            else: 
                duplicate = False
                for existingArticle in mergedArticleList: #if there are duplicates, do not add the element again but add the tag to the element
                    if existingArticle.title == article.title:
                        duplicate = True
                        if article.tags[0] not in existingArticle.tags:
                            existingArticle.tags.append(article.tags[0])
                        break

                if not duplicate:
                    mergedArticleList.append(article)

    return mergedArticleList

def setDefaultCategory(categories, categoryName):
    defaultSet = False
    for category in categories:
        if (category.name.lower() == categoryName.lower()) and (not defaultSet):
            category.default = True
            defaultSet = True
        else:
            category.default = False

    if not defaultSet:
        raise ValueError("categoryName " + categoryName + " does not exist within categories")

def getDefaultCategory(categories):
    for index, category in enumerate(categories):
        if category.default:
            return index
    if index is None:
        raise ValueError("No default category specified")