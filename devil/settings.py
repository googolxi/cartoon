# -*- coding: utf-8 -*-

# Scrapy settings for devil project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'devil'

SPIDER_MODULES = ['devil.spiders']
NEWSPIDER_MODULE = 'devil.spiders'
ITEM_PIPELINES = {
    'devil.pipelines.DevilPipeline': 1
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'devil (+http://www.yourdomain.com)'
