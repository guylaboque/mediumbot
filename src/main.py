from datetime import date, timedelta
import logging
import json
import time
import sys
import pathlib

import mediumcrawler as mcr
import telegramsender as tgs

scrapingConfig = pathlib.Path(__file__).parent.parent.resolve().joinpath('scraping_config.json')
try: #   Import scraping config
   with scrapingConfig.open('r') as f:
        config = json.load(f)

        daysSincePublishing = config['daysSincePublishing']
        tags = config['searchTags']
        keywords = config['keywords']
        blacklist = config['blacklist']
        minLikes = config['minLikes']
        configCategories = config['categories']
        
        categories = []
        for category in configCategories:
            newCategory = mcr.categories.Category(category["name"], category["keywords"], category["order"])
            categories.append(newCategory)
        categories.sort(key=lambda x: x.order) #sort categories by order  
        mcr.crawler.setDefaultCategory(categories, config['defaultCategory']) #set default category
except Exception:
    logging.exception("Something went wrong while reading the scraping config")
    sys.exit(1)

crawlDate = date.today() - timedelta(days=daysSincePublishing) #calculate crawl date

botConfig = pathlib.Path(__file__).parent.parent.resolve().joinpath('bot_config.json')
try: #   Import telegram bot config
    with botConfig.open('r') as f:
        telegramConfig = json.load(f)

        BOT_TOKEN = telegramConfig['BOT_TOKEN']
        CHAT_ID = telegramConfig['CHAT_ID']
except Exception:
        logging.exception("Something went wrong while reading the bot config")
        sys.exit(1)

#  Logging
logging.basicConfig(filename = str(pathlib.Path(__file__).parent.parent.resolve().joinpath('telegram_bot_logs.log')), level=logging.DEBUG)
logging.info('\nBot successfully started on ' + str(date.today()))

articleList = [] #initiate list for all articles in all tags and categories

for tag in tags: #Get list of all relevant articles for all tags
    try:
        articlesInTag = mcr.crawler.getArticles(tag, crawlDate) #Get articles for tag
        articlesInTag = mcr.listfilters.filterKeywords(articlesInTag, keywords, ["title"], keep=True) #Apply filters
        articlesInTag = mcr.listfilters.filterKeywords(articlesInTag, blacklist, ["title", "author"], keep=False) #Apply filters
        articlesInTag = mcr.listfilters.filterLikes(articlesInTag, minLikes) #Apply filters
        articleList = mcr.crawler.mergeArticleLists(articleList, articlesInTag) #Add to articles of other tags
    except Exception:
        logging.exception("Something went wrong with the medium crawler in tag " + tag)
    time.sleep(3)

for article in articleList: #distribute articles to categories
    distributed = False
    for category in categories:
        if  article.checkKeywords(category.keywords, ["title", "tags", "author"], ) and not category.default: #Add to first category that hits a keyword and is not the default category
            category.addArticle(article)
            distributed = True
            break
    if distributed is False:
        categories[mcr.crawler.getDefaultCategory(categories)].addArticle(article) #if there is no matching category, add to last category (=uncategorized)

try: # Send telegram message in main channel
    telegramMessageHeader = tgs.createMessageHeader(tags, keywords, crawlDate, minLikes)
    telegramMessageBody = tgs.createMessageBody(categories)
    telegramMessage = telegramMessageHeader + telegramMessageBody
    message = tgs.sendMessage(BOT_TOKEN, CHAT_ID, telegramMessage)
except Exception:
    logging.exception("Something went wrong with the telegram sender")
    sys.exit(1)
