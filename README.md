# mediumbot

## Purpose

The crypto space is often to fast to keep track of. Never miss the start of a cool farming opportunity or the genesis group of a new project again! 
Most projects host their blog at [medium](https://medium.com/.com/), so this bot scrapes through the blog posts, filters them for interesting opportunities and sends the results to a telegram group (click [here](https://t.me/joinchat/O5aS5xkp0zI4Zjli) to join).

<img src="https://user-images.githubusercontent.com/82145013/129738985-201911e9-1b15-4eab-adf5-0840a1c3e50e.jpeg" width="250">

## Configuration

The parameters for the scraping are found in the [scraping config](scraping_config.json):
* **daysSincePublishing:** Scrapes articles from these many days ago
* **tags:** Only articles with these tags are searched
* **keywords:** For all articles within the tags, only articles containing at least one of these keywords are recorded
* **blacklist:** If there are obvious scam-projects or article spammers, project containing these keywords will not be recorded
* **likeThreshold:** To filter for projects with certain traction, projects with at least this many likes are displayed at the top of the telegram message

The parameters for the telegram bot should be saved in a separate private file called bot_config.json in the root folder since especially the bot token should not be shared. The file should have the following format:
```json
{
    "BOT_TOKEN": "telegramBotToken",
    "CHAT_ID": "telegramChatId"
}
```

## Automation
If you want to automate the bot, you can do so e.g. by creating a cronjob for [pi_run.sh](run/pi_run.sh) on a raspberry pi. The pi_run.sh script:
* Pulls the latest version of the scraping config from github
* Executes the main script and sends it to a telegrambot

**Remember to add the bot_config.json file as well as install beautifulsoup4 for python3 and create your [bot](https://core.telegram.org/bots) + chatgroup on telegram!**
