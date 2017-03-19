"""
本爬虫用于测试随机Cookies在高并发状态下的使用, 测试对象为豆瓣电影.
已知问题:
    当在测试时, 第一次访问并不会被封IP, 但是当你再次访问相同的资源时, 就会被检测出来并封IP.
    所以请在谨慎测试
"""

import random
import string
from fake_useragent import UserAgent

from scrapy.spiders import Spider, Request


class RandomCookies(Spider):
    name = 'douban'
    custom_settings = {'CONCURRENT_REQUESTS': 100,
                       'CONCURRENT_REQUESTS_PER_DOMAIN': 100,
                       'COOKIES_DEBUG': True}

    def start_requests(self):
        """产生最初的请求
        bid: 返回一个随机的bid值
        headers: 返回一个随机User-Agent的headers
        """
        ua = UserAgent()
        bid = lambda: "".join(random.sample(string.ascii_letters + string.digits, 11))
        headers = lambda: {'User-Agent': ua.random,
                           'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, * / *;q = 0.8',
                           'Accept-Encoding': 'gzip, deflate, sdch, br',
                           'Host': 'www.douban.com'
                           }
        urls = ('https://movie.douban.com/tag/2016?start={page}'.format(page=i) for i in range(0, 3860, 20))
        for index, url in enumerate(urls):
            yield Request(url=url,
                          callback=self.parse,
                          headers=headers(),
                          cookies={'bid': bid()},
                          )

    def parse(self, response):
        pass


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy runspider {filename}'.format(filename=__file__).split())
