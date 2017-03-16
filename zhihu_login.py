from scrapy.http import FormRequest
from scrapy.spiders import Spider


class Login(Spider):
    name = 'zhihu_login'

    start_urls = ['https://www.zhihu.com']
    custom_settings = {'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64)'
                                     ' AppleWebKit/537.36 (KHTML, like Gecko)'
                                     ' Chrome/58.0.3026.3 Safari/537.36',
                       'COOKIES_DEBUG': True}

    def parse(self, response):
        formadata = {
            'password': '密码',
            'phone_num': '手机号',
            'email': '邮箱二选一, 不选的留空'
        }
        return FormRequest.from_response(
            url='https://www.zhihu.com/login/{}'.format('phone_num' if formadata['phone_num'] else 'email'),
            method="POST",  # 也是默认值, 其实不需要指定
            response=response,
            formxpath='//form[1]',  # 使用第一个form, 其实就是默认的, 这里明确写出来
            formdata=formadata,  # 我们填写的表单数据
            callback=self.after_login,  # 登录完成之后的处理
            dont_click=True)

    def after_login(self, response):
        import json
        result = json.loads(response.text)
        print(result)


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute('scrapy runspider {}'.format(__file__).split())
