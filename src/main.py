from datetime import date, timedelta
import logging
import json

import mediumcrawler as mcr
import telegramsender as tgs

## Set parameters
#   Import scraping config
with open('scraping_config.json', 'r') as f:
    config = json.load(f)

    daysSincePublishing = config['daysSincePublishing']
    tags = config['tags']
    keywords = config['keywords']
    blacklist = config['blacklist']
    likeThreshold = config['likeThreshold']

crawlDate = date.today() - timedelta(days=daysSincePublishing)

#   Import telegram bot config
with open('bot_config.json', 'r') as f:
    telegramConfig = json.load(f)

    BOT_TOKEN = telegramConfig['BOT_TOKEN']
    CHAT_ID = telegramConfig['CHAT_ID']

#   Create telegram styling and header
tagEmoji = '\U0001F3F7' #to set before the tag explanation
keywordEmoji = '\U0001F511'	 #to set before the keyword explanation
likesEmoji = '\U0001F44D' #to set before the likes explanation

telegramNewLine = '---------------------------------------'
telegramDateHeader = '<b><u>Medium articles from ' + str(crawlDate) + '</u></b>'
telegramTagHeader = tagEmoji + ' <b>Tags:</b> ' + ', '.join(tags)
telegramKeywordHeader = keywordEmoji + ' <b>Keywords:</b> ' +  ', '.join(keywords)
telegramLikesHeader = likesEmoji + ' <b>Min likes:</b> ' + str(likeThreshold+1)
telegramMessageHeader = telegramNewLine +  '\n' + telegramDateHeader + '\n' + telegramTagHeader + '\n' + telegramKeywordHeader + '\n' + telegramLikesHeader + '\n' + telegramNewLine

#  Logging
logging.basicConfig(filename='telegram_bot_logs.log', level=logging.DEBUG)
logging.info('\nBot successfully started on ' + str(date.today()))

## Crawl relevant Medium pages for articles matching the filters
articleList = [] #initiate list for all articles in all tags
for url in mcr.urls.getTagUrls(tags, crawlDate): #for all pages corresponding to defined tags
    articlesInTag = mcr.crawler.getArticles(url)
    filteredArticlesInTag = mcr.filters.filterBlacklist(mcr.filters.filterKeywords(articlesInTag, keywords), blacklist)
    articleList += filteredArticlesInTag

articleList = list(set(articleList)) #remove duplicate entries

## Send telegram message
telegramMessageHtml = tgs.createHtmlMessage(articleList, telegramMessageHeader, likeThreshold)
messageSent = tgs.sentTelegramMessage(BOT_TOKEN, CHAT_ID, telegramMessageHtml)
