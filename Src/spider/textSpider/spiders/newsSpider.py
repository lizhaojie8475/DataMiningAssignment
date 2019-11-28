# -*- coding: utf-8 -*-
import sys
sys.path.append("E:\\lizhaojie\\DataMiningAssignment")
import scrapy
from scrapy.http import Request
import time
from Src.spider.textSpider.items import NewsItem


SUM_OF_DAYS = 500
CURRENT_DATE = "2011-11-23"

class NewsspiderSpider(scrapy.Spider):
    name = 'newsSpider'

    def __init__(self, category, *args, **kwargs):
        super().__init__(*args, **kwargs)
        timeArray = time.strptime(CURRENT_DATE, '%Y-%m-%d')
        self.day = 0
        self.category = category
        self.currentTime = int(time.mktime(timeArray))


    def start_requests(self):
        for i in range(SUM_OF_DAYS):
            self.currentTime -= 86400
            dateStr = self.parseDate(time.localtime(self.currentTime))
            url = "http://www.chinanews.com/scroll-news/%s/news.shtml" % dateStr
            yield Request(url=url, meta={"time": dateStr})

    def parseDate(self, date):
        year = date[0]
        month = date[1]
        day = date[2]
        if month < 10:
            month = "0" + str(month)
        else:
            month = str(month)

        if day < 10:
            day = "0" + str(day)
        else:
            day = str(day)

        return str(year) + '/' + month + day

    def parse(self, response):
        titleSelectors = response.selector.xpath('//*[@id="content_right"]/div[@class = "content_list"]/ul/li')
        for selector in titleSelectors:
            type = selector.xpath('./div[1]/a[1]/text()').extract_first()
            title = selector.xpath('./div[2]/a[1]/text()').extract_first()
            time = response.meta["time"]
            url = selector.xpath('./div[2]/a[1]/@href').extract_first()
            if url == None or str(url).find('http') != -1 :
                continue
            url = "http://www.chinanews.com" + str(url)
            if type == self.category:
                item = NewsItem()
                item["title"] = title
                item["type"] = type
                item["url"] = url
                item["time"] = time
                yield Request(url=url, meta={"item": item}, callback=self.parseContent)

    def parseContent(self, response):
        contentSelector = response.xpath('//*[@id="cont_1_1_2"]/div[@class = "left_zw"]/p/text()')
        paragraphs = filter(lambda x: len(x) >= 25, contentSelector.extract())
        paragraphs = map(lambda x: x.strip().replace(r"\s+", ""), paragraphs)
        content = "".join(paragraphs)
        if len(content) > 2000:
            content = content[:2000]

        item = response.meta["item"]
        item["content"] = content
        yield item