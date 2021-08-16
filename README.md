# mediumbot

## Purpose

The crypto space is often to fast to keep track of. Never miss the start of a cool farming opportunity or the genesis group of a new project again! 
Most projects host their blog at [GitHub Pages](https://medium.com/.com/), so this bot scrapes through the blog posts and filters them for interesting opportunities and sends the results to a telegram group.

## Parameters

The parameters for the scraping are found in the config file:
* **daysSincePublishing:** Scrapes articles from these many days ago
* **tags:** Only articles with these tags are searched
* **keywords:** For all articles within the tags, only articles containing at least one of these keywords are recorded
* **blacklist:** If there are obvious scam-projects or article spammers, project containing these keywords will not be recorded
* **likeThreshold:** To filter for projects with certain traction, projects with at least this many likes are displayed at the top of the telegram message
