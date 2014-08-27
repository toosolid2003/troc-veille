# -*- coding: utf-8 -*-

# Scrapy settings for veilleTroc project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'veilleTroc'

SPIDER_MODULES = ['veilleTroc.spiders']
NEWSPIDER_MODULE = 'veilleTroc.spiders'
USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'veilleTroc (+http://www.yourdomain.com)'
