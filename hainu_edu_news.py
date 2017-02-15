# -*- coding: utf-8 -*-

import scrapy
from pymongo import MongoClient
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from scrapy.spiders import CrawlSpider, Rule


class NewsItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()


class NewsSpider(CrawlSpider):
    name = 'news'
    debug_mode = True
    allowed_domains = ['hainu.edu.cn']
    start_urls = ['http://www.hainu.edu.cn/stm/vnew/shtml_liebiao.asp@bbsid=2439.shtml']
    # 取消重试, 有些网页以及移除了, 重试浪费时间
    # 如果是调试, 请开启缓存, 避免对服务器造成压力, 而且调试速度更快
    custom_settings = {'RETRY_ENABLED': False, 'HTTPCACHE_ENABLED': True, 'CONCURRENT_REQUESTS': 50}
    rules = (
        Rule(LinkExtractor(restrict_css=['.liebiao1ul']), callback='list_page', follow=True),
        Rule(LinkExtractor(restrict_xpaths=['//div[@class="news_list clearfix"]']), callback='content_page'),
        Rule(LinkExtractor(restrict_xpaths=['//a[text()=">>"]']), follow=True),
    )

    def __init__(self):
        super().__init__()
        # 连接Mongodb
        self.MongoURI = 'mongodb://localhost:27017'
        self.client = MongoClient(self.MongoURI)
        self.db = self.client[self.__class__.__name__]
        self.collection = self.db[self.name]
        # 如果是调试模式, 每次启动前都会drop collection, 防止数据混杂在一起
        if self.debug_mode:
            self.collection.drop()

    def content_page(self, response, ):
        l = ItemLoader(item=NewsItem(), response=response)
        l.default_input_processor = MapCompose(str.strip)
        l.default_output_processor = TakeFirst()
        l.add_xpath('title', '//*[@class="biaoti"]/text()')
        l.add_xpath('title', '//title/text()')
        l.add_xpath('date', '//text()', re=r'\d+[/-]\d+[/-]\d+ \d+:\d+:\d+')
        l.add_xpath('source', '//text()', re=r'来源：\s*(\S+)')
        l.add_value('url', response.url)
        item = l.load_item()
        self.collection.insert_one(dict(item))
        yield item


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy runspider hainu_edu_news.py'.split())
