# Define filter functions
def filterKeywords(articles, keywords, fields, keep=True): #filter for keywords
    filteredArticles = []
    for article in articles:
        if article.checkKeywords(keywords, fields) is keep:
            filteredArticles.append(article)
    
    return(filteredArticles)

def filterLikes(articles, likeThreshold):
    filteredArticles = []
    for article in articles:
        if int(article.likes) >= int(likeThreshold):
            filteredArticles.append(article)
            
    return filteredArticles