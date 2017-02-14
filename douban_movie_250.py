# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Compose
from scrapy.spiders import CrawlSpider


class MovieItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    rating_num = scrapy.Field()
    rating_people = scrapy.Field()
    quote = scrapy.Field()


class MovieSpider(CrawlSpider):
    name = 'movie_250'
    allowed_domains = ['movie.douban.com']
    custom_settings = {'USER_AGENT': 'Mozilla/5.0'}
    download_delay = 2.0
    start_urls = ['https://movie.douban.com/top250?start={page}'.format(page=page)
                  for page in range(0, 26, 25)]

    def parse(self, response):
        for movie in response.xpath('//div[@class="item"]'):
            l = ItemLoader(item=MovieItem(), response=response, selector=movie)
            l.default_output_processor = Compose(TakeFirst(), lambda out: out.replace('\xa0', ''))
            l.add_xpath('title', 'normalize-space(.//div[@class="hd"])')
            l.add_xpath('link', './/div[@class="hd"]/a/@href')
            l.add_xpath('rating_num', './/span[@class="rating_num"]/text()')
            l.add_xpath('rating_people', './/text()[contains(., "人评价")]')
            l.add_xpath('quote', './/span[@class="inq"]/text()')
            item = l.load_item()
            yield item


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy runspider douban_movie_250.py'.split())
