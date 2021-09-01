## FUNCTIONS USED TO CREATE MESSAGES TO SEND ON TELEGRAM

from os import name
import requests
import urllib
import html
import logging

# Styling
emojis = {
    "dividerEmoji": '\U0001F5C2',
    "tagEmoji": '\U0001F3F7',
    "keywordEmoji": '\U0001F511',
    "likeEmoji": '\U0001F44D'
}

lineBreak = '---------------------------------------\n'

def cleanHtml(text):
    return urllib.parse.quote(html.escape(text))

# Create HTML message
def createMessageHeader(tags, keywords, crawlDate, minLikes):     #   Create telegram styling and header

    dateHeader = '<b><u>Medium articles from ' + str(crawlDate) + '</u></b>\n'
    tagHeader = emojis["dividerEmoji"] + ' <b>Tags:</b> ' + ', '.join(tags) + '\n'
    keywordHeader = emojis["keywordEmoji"] + ' <b>Keywords:</b> ' +  ', '.join(keywords) + '\n'
    likesHeader = emojis["likeEmoji"] + ' <b>Min likes:</b> ' + str(minLikes)
    #messageHeader = lineBreak  + dateHeader + tagHeader + keywordHeader + likesHeader + lineBreak
    messageHeader = dateHeader + likesHeader
    
    return messageHeader

def createCategoryHeader(category):
    categoryHeader = '\n' + lineBreak + emojis["tagEmoji"] + "<b>" + cleanHtml(category.name) + "</b>" + '\n' + lineBreak
    return categoryHeader

def createArticleEntry(article):
    articleEntry = '\n<a href="' + article.titlelink + '">' + cleanHtml(article.title) + '</a>\n(<a href="' + article.authorlink + '">' + cleanHtml(article.author) + '</a>, likes: '+ article.likes + ')\n'
    return articleEntry

def createMessageBody(categories):
    telegramBody = ""
    for category in categories:
        if len(category.articles) >= 1:
            telegramBody += createCategoryHeader(category)
            for article in category.articles: #all articles above likesThreshold
                telegramBody += createArticleEntry(article)

    return telegramBody

# Send telegram message
def sendMessage(botToken, chatId, bot_message):
    send_text = 'https://api.telegram.org/bot' + botToken + '/sendMessage?chat_id=' + chatId + '&parse_mode=HTML&disable_web_page_preview=true&text=' + bot_message

    response = requests.get(send_text).json()

    if response['ok'] is True:
        logging.info('Telegram message successfully sent to the main channel!')
    else:
        logging.error('Error sending telegram message: ' + str(response))

    return response
