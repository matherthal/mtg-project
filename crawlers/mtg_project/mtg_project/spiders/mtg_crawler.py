# -*- coding: utf-8 -*-
from scrapy import Spider
from mtg_project.items import DeckItem

import logging
from time import strptime

class MtgCrawlerSpider(Spider):
    name = "mtg_crawler"
    allowed_domains = ["mtgtop8.com"]
    start_urls = [
        "http://www.mtgtop8.com/search",
    ]

    def parse(self, response):
        decks = response.xpath('//table[@class="Stable"]/tr[@class="hover_tr"]')
        
        for index, deck in enumerate(decks):
            item = DeckItem()

            item['deck_name'] = deck.xpath('td[2]/a/text()').extract_first()
            item['player'] = deck.xpath('td[3]/a/text()').extract_first()
            item['championship'] = deck.xpath('td[4]/a/text()').extract_first()
            item['rank'] = deck.xpath('td[6]/text()').extract_first()
            item['date'] = deck.xpath('td[7]/text()').extract_first()

            #count level (ie number of stars or bigstar)
            stars = deck.xpath('td[5]').css('img').xpath('@src').extract()
            count = 0
            for star in stars:
                if stars == "graph/bigstar.png":
                    count = 4
                    break
                count += 1
            item['level'] = count

            yield item
