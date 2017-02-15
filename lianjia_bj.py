# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from scrapy.spiders import CrawlSpider, Rule
from fake_useragent import UserAgent
from scrapy.settings import default_settings


class LianjiaItem(scrapy.Item):
    # 标签  小区  户型   面积  朝向  装修 关注人数  观看人数  发布时间  价格   均价  详情链接
    title = scrapy.Field()
    community = scrapy.Field()
    model = scrapy.Field()
    area = scrapy.Field()
    direction = scrapy.Field()
    decoration = scrapy.Field()
    focus_num = scrapy.Field()
    watch_num = scrapy.Field()
    time = scrapy.Field()
    price = scrapy.Field()
    average_price = scrapy.Field()
    link = scrapy.Field()


class LianjiaSpider(CrawlSpider):
    name = 'lianjia'
    download_delay = 3.0
    ua = UserAgent()
    custom_settings = {'USER_AGENT': ua.random, 'HTTPCACHE_ENABLED': True, 'COOKIES_ENABLED': False}
    start_urls = ['http://bj.lianjia.com/ershoufang/']

    def parse(self, response):
        for area in response.xpath('//div[@data-role="ershoufang"]//a/@href'):
            rel_link = area.extract()
            yield scrapy.Request(url=response.urljoin(rel_link), callback=self.next_page,
                                 headers={'USER_AGENT': self.ua.random})

    def next_page(self, response):

        page_url = response.xpath('//@page-url').extract_first()
        page_data = response.xpath('//@page-data').extract_first()
        # total_page = eval(page_data)['totalPage']
        total_page = 2
        for page in range(1, total_page + 1):
            rel_url = page_url.format(page=page)
            yield scrapy.Request(url=response.urljoin(rel_url), callback=self.parse_item,
                                 headers={'USER_AGENT': self.ua.random})

    def parse_item(self, response):
        for house in response.xpath('//ul[@sellListContent]/li'):
            l = ItemLoader(item=LianjiaItem(), response=response, selector=house)
            l.default_output_processor = TakeFirst()
            l.add_xpath('title', './/div[@class="title"]/a/text()')
            l.add_xpath('community', './/div[class="houseInfo""]/a/text()')
            l.add_xpath('model', './/div[@class="houseInfo"]/text()', re=r'\d室\d厅')
            l.add_xpath('area', './/div[@class="houseInfo"]/text()', re=r'[\d\.]+平米')
            l.add_xpath('direction', './/div[@class="houseInfo"]/text()', re=r'[东西南北 ]+')
            l.add_xpath('decoration', './/div[@class="houseInfo"]/text()', re=r'.装')
            l.add_xpath('focus_num', './/div[@class="followInfo"]/text()', re=r'\d+人关注')
            l.add_xpath('watch_num', './/div[@class="followInfo"]/text()', re=r'共\d+次带看')
            l.add_xpath('time', './/div[@class="followInfo"]/text()', re=r'[\W]+以前发布')
            l.add_xpath('price', './/div[@class="totalPrice"]/span/text()')
            l.add_xpath('average_price', './/div[@class="unitPrice"]/@data-price')
            l.add_xpath('link', './/div[@class="title"]/a/@href')
            item = l.load_item()
            yield item
            print(item)


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy runspider lianjia_bj.py'.split())
