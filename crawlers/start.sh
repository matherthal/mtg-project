scrapy startproject mtg_project 
 
scrapy genspider mtg_crawler mtgtop8.com/search -t crawl
 
 
scrapy crawl mtgcrawlerspider