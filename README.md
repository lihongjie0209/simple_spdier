# simple_spdier

## 本仓库主要用于存储Scrapy单只爬虫(非一个完整项目),现在包含以下爬虫:

 - 豆瓣电影TOP250(douban_movie_250.py)
 
 使用最简单的构造链接的方式进行翻页, 对数据中的非法字符进行了简单的清理. 
 
爬取数据格式为:
 ```python

 {'link': 'https://movie.douban.com/subject/1292215/',
 'quote': '法式小清新。 ',
 'rating_num': '8.7',
 'rating_people': '449237人评价',
 'title': "天使爱美丽 /Le fabuleux destin d'Amélie Poulain /艾蜜莉的异想世界(台) / 天使艾米莉 "
          '[可播放]'}
 ```
---
 - 海南大学新闻(hainu_edu_news.py)
 
 使用`crawlspider`对海南大学新闻板块的六个子板块进行的爬取, 对于各个板块不同的的HTML格式, 使用正则表达式进行数据的抽取. 
 
 爬取数据格式(Mongodb)为:

```python
 {
    "_id" : ObjectId("58a4332b2973ab74d3d26262"),
    "source" : "党办",
    "url" : "http://www.hainu.edu.cn/stm/vnew/20161231/10470560.shtml",
    "date" : "2017/2/8 12:12:00",
    "title" : "海南大学2017年新年贺词"
}
```
---

- 链家北京二手房(lianjia_bj.py), 爬取格式数据格式为:

使用`crawlspider`对北京链家二手房数据进行爬取, 以不同的城区作为入口, 使用`Rule`指定爬取规则, 使用Xpath配合正则表达式抽取数据.
 

```python
{'area': '83.87平米',
 'average_price': '101348',
 'community': '东直门内北小街8号院 ',
 'decoration': '简装',
 'direction': '西',
 'focus_num': '60人关注',
 'link': 'http://bj.lianjia.com/ershoufang/101100919031.html',
 'model': '2室1厅',
 'price': '850',
 'title': '满五且一套房产，景山学校北校区划片范围 电梯直达',
 'watch_num': '共56次带看'}
```
---
- 知乎登录(zhihu_login.py)

通过抓包分析登录过程, 使用`FormRequest`获取登录提交表单并模拟提交.
登录之后的Cookies数据保存在Cookies Jar中, 默认在之后的所有链接中使用.

使用方法:

   - 在`parser`函数中中的`formdata` 填入你的登录信息.
   - 使用 `python zhihu_login.py`启动爬虫.
   - 默认情况下打印知乎返回的登录状态码
---
- 随机Cookies

本爬虫用于测试随机Cookies在高并发状态下的使用, 测试对象为豆瓣电影.
已知问题:
    当在测试时, 第一次访问并不会被封IP, 但是当你再次访问相同的资源时, 就会被检测出来并封IP.
    所以请在谨慎测试

## 使用方法:

下载对应文件, 然后`python 文件名.py`. 如需调整相应参数, 请在文件结尾处修改即可:

```python
if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy runspider hainu_edu_news.py'.split())
```