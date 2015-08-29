# -*- coding: utf-8 -*-
from mtg_project.items import DeckItem
from mtg_project.items import CardItem

from scrapy import Spider
# from scrapy.spiders import CrawlSpider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.http import Request 

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

            # get profile url
            deck_url = deck.xpath('td[2]/a/@href').extract_first()
            # join with base url since profile url is relative
            follow = urljoin_rfc(base_url, deck_url)

            yield Request(follow, callback = self.parse_cards, meta={'item':item})
            
            # yield item


        # next_page = response.css("ul.navigation > li.next-page > a::attr('href')")
        # if next_page:
        #     url = response.urljoin(next_page[0].extract())
        #     yield Request(url, self.parse_articles_follow_next_page)

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
