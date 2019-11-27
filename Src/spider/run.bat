@echo off

::scrapy crawl newsSpider -a category=文化
::scrapy crawl newsSpider -a category=社会
::scrapy crawl newsSpider -a category=军事
scrapy crawl newsSpider -a category=国际
::scrapy crawl newsSpider -a category=健康
::scrapy crawl newsSpider -a category=财经
::scrapy crawl newsSpider -a category=I  T
::scrapy crawl newsSpider -a category=娱乐
::scrapy crawl newsSpider -a category=体育

pause
