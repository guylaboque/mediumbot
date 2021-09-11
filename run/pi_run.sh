#!/bin/bash

# A simple shell script to update the telegram search parameters of the bot and run it afterwards

cd "$(dirname "$0")"
cd ..
wget --output-document=scraping_config.json --append-output=telegram_bot_logs.log https://raw.githubusercontent.com/guylaboque/mediumbot/main/scraping_config.json || true # Pull new scraping config file
cd src
python3 main.py # Run medium scraper bot
