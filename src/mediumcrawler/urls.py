## FUNCTIONS USED TO FACILITATE CRAWLING THE MEDIUM PAGES

# Find urls for medium
def getTagUrl(tag, postDate):
    return 'https://medium.com/tag/' + tag.lower() + '/archive/' + postDate.strftime("%Y/%m/%d")