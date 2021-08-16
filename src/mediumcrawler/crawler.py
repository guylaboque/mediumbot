import requests
import logging
from bs4 import BeautifulSoup

from .article import MediumArticle

def getArticles(url):
    response = requests.get(url)
    mediumPage = BeautifulSoup(response.text, 'html.parser')

    articleElements = mediumPage.findAll('div', attrs={"class":"postArticle--short"}) #get whole elements for blog posts

    articles = []

    for blogPost in articleElements:

        title_check = blogPost("h3", "graf--title")
        if not title_check: #skip articles without a title
            continue
        title = str(title_check[0].string) #create comparable string of title

        link = blogPost("a", attrs={"data-action": "open-post"})[0].get('href').split("?")[0]
        likeData = blogPost("button", attrs={"data-action": "show-recommends"})

        if not likeData:
            likes = "0"
        else:
            likes = str(likeData[0].string)

        article = MediumArticle(title, link, likes)
        articles.append(article)

    if len(articles) == 0:
        logging.warning("No articles found, maybe something changed in the page structure")

    return articles