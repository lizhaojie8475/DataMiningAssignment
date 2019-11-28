from scrapy.cmdline import execute

execute(["scrapy", "crawl", "newsSpider", "-a", "category=auto"])