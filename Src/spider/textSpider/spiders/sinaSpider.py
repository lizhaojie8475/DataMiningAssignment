# -*- coding: utf-8 -*-
import sys
sys.path.append("E:\\lizhaojie\\DataMiningAssignment")
import scrapy
from scrapy.http import Request
import time
from Src.spider.textSpider.items import NewsItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re


class SinaspiderSpider(scrapy.Spider):
    name = 'sinaSpider'
    start_urls = ['http://news.cctv.com/tech/?spm=C94212.P4YnMod9m2uD.0.0']

    def start_requests(self):
        return [Request(self.start_urls[0], meta={"url": self.start_urls[0]})]

    def parse(self, response):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        browser = webdriver.Chrome(executable_path='E:\\lizhaojie\\DataMiningAssignment\\chromedriver.exe', chrome_options=chrome_options)
        browser.get(response.meta["url"])
        time.sleep(5)
        titleList = browser.find_elements_by_xpath('//li[contains(@style, "display")]//h3[@class="title"]/a')
        for title in titleList:
            url = title.get_attribute("href")
            title = title.text
            type = "科技"
            item = NewsItem()
            item["url"] = url
            item["type"] = type
            item["title"] = title
            yield Request(url=url, meta={"item": item}, callback=self.parseContent)

        while(1):
            try:
                loadBotton = browser.find_element_by_xpath('//div[@class="more"]//p')
                loadBotton.click()
            except:
                time.sleep(2)
                continue
            finally:
                time.sleep(1)

            titleList = browser.find_elements_by_xpath('//li[contains(@style, "display")]//h3[@class="title"]/a')
            titleList = titleList[-20: -1]
            for title in titleList:
                url = title.get_attribute("href")
                title = title.text
                type = "科技"
                item = NewsItem()
                item["url"] = url
                item["type"] = type
                item["title"] = title
                yield Request(url=url, meta={"item": item}, callback=self.parseContent)


    def parseContent(self, response):
        contentSelector = response.xpath('//div[@class="content_area" and @id="content_area"]//p/text()')
        contentList = contentSelector.extract()
        paragraphs = filter(lambda x: len(x) >= 20, contentList)
        paragraphs = map(lambda x: x.strip().replace(r"\s+", ""), paragraphs)

        content = "".join(paragraphs)
        if len(content) > 2000:
            content = content[:2000]

        item = response.meta["item"]
        item["content"] = content

        timeStr = response.xpath('//*[@id="title_area"]/div[@class="info1"]/text()').extract_first()
        time = re.search(r"(\d+年.*)", timeStr).group(1)
        item["time"] = time

        yield item

