## FUNCTIONS USED TO FACILITATE CRAWLING THE MEDIUM PAGES

# Find urls for medium
def getTagUrls(tags, postDate):
    mediumUrls = []
    for tag in tags:
        mediumUrls.append('https://medium.com/tag/' + tag + '/archive/' + postDate.strftime("%Y/%m/%d"))

    return mediumUrls