# simple_spdier

## 本仓库主要用于存储Scrapy单只爬虫(非一个完整项目),现在包含以下爬虫:

 - 豆瓣电影TOP250(douban_movie_250.py), 爬取数据格式为:

 ```python

 {'link': 'https://movie.douban.com/subject/1292215/',
 'quote': '法式小清新。 ',
 'rating_num': '8.7',
 'rating_people': '449237人评价',
 'title': "天使爱美丽 /Le fabuleux destin d'Amélie Poulain /艾蜜莉的异想世界(台) / 天使艾米莉 "
          '[可播放]'}
 ```

 - 海南大学新闻(hainu_edu_news.py), 爬取数据格式为:

```python
 {
    "_id" : ObjectId("58a4332b2973ab74d3d26262"),
    "source" : "党办",
    "url" : "http://www.hainu.edu.cn/stm/vnew/20161231/10470560.shtml",
    "date" : "2017/2/8 12:12:00",
    "title" : "海南大学2017年新年贺词"
}
```

## 使用方法:

下载对应文件, 然后`python 文件名.py`. 如需调整相应参数, 请在文件结尾处修改即可:

```python
if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy runspider hainu_edu_news.py'.split())
```