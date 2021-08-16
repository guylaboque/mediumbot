## FUNCTIONS USED TO CREATE MESSAGES TO SEND ON TELEGRAM

import requests
import urllib
import html
import logging

# Create HTML message to send via telegram
def createHtmlMessage(articleList, telegramMessageHeader, likesThreshold):
    telegramMessageHtml = telegramMessageHeader

    lessLikesEmoji = '\U0001F44E'

    articleList.sort(key= lambda article: int(article.likes), reverse=True) #sort by likes

    for article in articleList: #all articles above likesThreshold
        if int(article.likes) > likesThreshold:
            htmlTitle = urllib.parse.quote(html.escape(article.title))
            telegramMessageHtml += '\n<a href="' + article.link + '">' + htmlTitle + '</a> (likes: '+ article.likes + ')\n'

    telegramMessageHtml += "\n---------------------------------------\n" + lessLikesEmoji + " <b>Articles with " + str(likesThreshold) + " likes or less:</b>\n---------------------------------------\n"

    for article in articleList: #all articles below likesThreshold
        if int(article.likes) <= likesThreshold:
            htmlTitle = urllib.parse.quote(html.escape(article.title))
            telegramMessageHtml += '\n<a href="' + article.link + '">' + htmlTitle + '</a> (likes: '+ article.likes + ')\n'

    return telegramMessageHtml

# Send telegram message
def sentTelegramMessage(botToken, botChatId, bot_message):
    send_text = 'https://api.telegram.org/bot' + botToken + '/sendMessage?chat_id=' + botChatId + '&parse_mode=HTML&disable_web_page_preview=true&text=' + bot_message

    response = requests.get(send_text).json()

    if response['ok'] is True:
        logging.info('Telegram message successfully sent!')
    else:
        logging.error('Error sending telegram message: ' + str(response))

    return response
