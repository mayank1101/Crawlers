# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class AstroItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    links = scrapy.Field()
    questions = scrapy.Field()
    votes = scrapy.Field()
    no_answers = scrapy.Field()
    tags = scrapy.Field()
