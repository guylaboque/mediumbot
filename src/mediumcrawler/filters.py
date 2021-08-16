# Define filter functions
def filterKeywords(articles, keywords): #filter for keywords
    filteredArticles = []
    for article in articles:
        if any(item in article.title.lower() for item in keywords):
            filteredArticles.append(article)
    
    return(filteredArticles)


def filterBlacklist(articles, blacklist): #filter for blacklisted words
    filteredArticles = []
    for article in articles:
        if not any(item in article.title.lower() for item in blacklist):
            filteredArticles.append(article)
    
    return(filteredArticles)