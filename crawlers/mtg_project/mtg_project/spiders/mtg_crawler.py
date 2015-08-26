# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# from scrapy.selector import HtmlXPathSelector
from scrapy import Selector
import logging

from mtg_project.items import DeckItem

class MtgCrawlerSpider(CrawlSpider):
    name = 'mtg_crawler'
    allowed_domains = ['mtgtop8.com']
    start_urls = ['http://www.mtgtop8.com/search']
    # start_urls = ['http://mtgtop8.com/event?e=10022&f=LE']

    rules = (
        Rule(LinkExtractor(allow=r'search'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        hxs = Selector(response)

        decks = hxs.xpath('//table[@class="Stable"]/tbody/tr[@class="hover_tr"]')
        for deck in decks:
            item = DeckItem()

            item['deck_name'] = deck.xpath('td[2]/a/text()').extract()[0]
            
            logging.info(item['deck_name'])

            item['player'] = deck.xpath('td[3]/a/text()').extract()[0]
            item['championship'] = deck.xpath('td[4]/a/text()').extract()[0]
            item['rank'] = deck.xpath('td[6]/a/text()').extract()[0]
            item['date'] = deck.xpath('td[7]/a/text()').extract()[0]

            #count level (ie number of stars or bigstar)
            stars = deck.xpath('td[5]')
            count = 0
            for star in stars:
                if star.xpath('img[contains(@src, "graph/bigstar.png")]'):
                    count = 4
                    break
                elif star.xpath('img[contains(@src, "graph/star.png")]'):
                    count += 1
            item['level'] = count

            # # get profile url
            # deck_url = deck.select('td[2]/a/@href').extract()[0]
            # # join with base url since profile url is relative
            # base_url = get_base_url(response)
            # follow = urljoin_rfc(base_url, deck_url)

            # request = Request(follow, callback = parse_deck)
            # request.meta['item'] = item
            
            yield item

    def parse_deck(self, response):
        item = response.meta['item']
        # item['address'] = figure out xpath
        return item





        # item['championship'] = response.xpath('//div[@class="w_title"]/table/tbody/tr/td[@class="S18"]/text()')[0].extract()[0]
        #item['player'] = response.xpath('//div[@class="w_title"]/table/tbody/tr/td[@class="S16"]/a[@class="player"]/text()')[0].extract()[0]
        
        #label = response.xpath('//div[@class="w_title"]/table/tbody/tr/td[@class="S16"]/text()')[0].extract()[0]
        #rank = label.replace('#', '').split(' ')[0]
        #item['player_rank'] = rank
        #item['deck_name'] = label.replace('#' + rank + ' ', '').replace(' - ', '')
        
        #cards = response.xpath('//table[@class="Stable"]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[@class="G14"]/div')
        # cards = response.xpath('//td[@class="G14"]/div')
        
        # for card in cards:
        #     item = MtgProjectItem()
        #     item['qtd_cards'] = card.xpath(
        #         'text()').extract()[0]
        #     item['card_name'] = card.xpath(
        #         'span[@class="L14"]/text()').extract()[0]
            
        #     yield item
