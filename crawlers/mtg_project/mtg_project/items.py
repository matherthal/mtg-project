# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DeckItem(scrapy.Item):

    championship = scrapy.Field()
    player = scrapy.Field()
    player_rank = scrapy.Field()
    deck_name = scrapy.Field()
    level = scrapy.Field()
    date = scrapy.Field()
    cards = scrapy.Field()