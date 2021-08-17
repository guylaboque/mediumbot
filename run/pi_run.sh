#!/bin/bash

# A simple shell script to update the telegram search parameters of the bot and run it afterwards

cd "$(dirname "$0")"
cd ..
sudo wget --output-document=scraping_config.json https://raw.githubusercontent.com/guylaboque/mediumbot/main/scraping_config.json # Pull new scraping config file
cd src
python main.py # Run medium scraper bot
