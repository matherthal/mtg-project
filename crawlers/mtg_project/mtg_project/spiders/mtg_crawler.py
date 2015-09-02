# -*- coding: utf-8 -*-
from mtg_project.items import DeckItem
from mtg_project.items import CardItem

from scrapy import Spider
# from scrapy.spiders import CrawlSpider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.http import Request, FormRequest 

import logging
# from time import strptime
import time
import math

class MtgCrawlerSpider(Spider):

    name = "mtg_crawler"
    allowed_domains = ["mtgtop8.com"]
    start_urls = [
        "http://www.mtgtop8.com/search",
    ]

    def parse(self, response):
        curr_page = 0
        total_decks = int(response.xpath('//div[@class="w_title"]/text()').extract_first().split()[0])
        decks_per_page = 25
        max_page = int(math.ceil(total_decks / float(decks_per_page)))

        for i in range(1,max_page+1):
            yield FormRequest.from_response(response, 
                formname='search_form', 
                formdata={'current_page': str(i)}, 
                callback=self.parse_deck)

    def parse_deck(self, response):
        decks = response.xpath('//table[@class="Stable"]/tr[@class="hover_tr"]')
        
        base_url = get_base_url(response)
        
        for index, deck in enumerate(decks):
            item = DeckItem()

            # get important information from the table
            item['deck_name'] = deck.xpath('td[2]/a/text()').extract_first()
            item['player'] = deck.xpath('td[3]/a/text()').extract_first()
            item['championship'] = deck.xpath('td[4]/a/text()').extract_first()
            item['rank'] = deck.xpath('td[6]/text()').extract_first()
            item['date'] = deck.xpath('td[7]/text()').extract_first()

            # count level (ie number of stars or bigstar)
            stars = deck.xpath('td[5]').css('img').xpath('@src').extract()
            count = 0
            for star in stars:
                if stars == "graph/bigstar.png":
                    count = 4
                    break
                count += 1
            item['level'] = count

            # get cards from this deck through this url
            deck_url = deck.xpath('td[2]/a/@href').extract_first()
            # join with base url since this url is relative
            follow = urljoin_rfc(base_url, deck_url)
            
            request = Request(follow, callback = self.parse_cards, meta={'item':item})

            yield request

    def parse_cards(self, response):
        item = response.meta['item']
        
        #DEBUG
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        
        item['format'] = response.xpath('//td[@class="S14"]/text()')[0].extract().strip()
        item['cards'] = []
        
        cards = response.xpath('//td[@class="G14"]')
        for index, card in enumerate(cards):
            card_item = CardItem()
            card_item['qtt'] = card.xpath('div/text()').extract_first()
            card_item['name'] = card.xpath('div/span/text()').extract_first()
            item['cards'].append(card_item)

        return item
