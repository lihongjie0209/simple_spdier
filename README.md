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

 - 海南大学新闻(hainu_edu_news.py), 爬取数据格式(Mongodb)为:

```python
 {
    "_id" : ObjectId("58a4332b2973ab74d3d26262"),
    "source" : "党办",
    "url" : "http://www.hainu.edu.cn/stm/vnew/20161231/10470560.shtml",
    "date" : "2017/2/8 12:12:00",
    "title" : "海南大学2017年新年贺词"
}
```

- 链家北京二手房(lianjia_bj.py), 爬取格式数据格式为:

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

- 知乎登录(zhihu_login.py)

使用五行代码登录知乎, 并保存cookies信息

## 使用方法:

下载对应文件, 然后`python 文件名.py`. 如需调整相应参数, 请在文件结尾处修改即可:

```python
if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy runspider hainu_edu_news.py'.split())
```