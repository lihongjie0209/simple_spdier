"""
This module is used for login zhihu.com.
You should enter your username and password in the parse function.

Example:

    python zhihu_login.py
"""

from scrapy.http import FormRequest
from scrapy.spiders import Spider


class Login(Spider):
    name = 'zhihu_login'
    start_urls = ['https://www.zhihu.com']

    # update default setting of user_agent and cookies_debug
    custom_settings = {'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64)'
                                     ' AppleWebKit/537.36 (KHTML, like Gecko)'
                                     ' Chrome/58.0.3026.3 Safari/537.36',
                       'COOKIES_DEBUG': True}

    def parse(self, response):
        """post data to the login page and return the response

        :param response: the response of start_urls
        :return: response object of login page

        the formdata is dict object which contains the login information
        Example:
        formdata = {
            'password': 'your password',
            'phone_num': 'your phone number',
        }

        or:
        formdata = {
            'password': 'your password',
            'email': 'your email address'
        }
        """
        formdata = {
            'password': '密码',
            'phone_num': '手机号',
            'email': '邮箱二选一, 不选的留空'
        }
        return FormRequest.from_response(
            url='https://www.zhihu.com/login/{}'.format('phone_num' if formdata.get('phone_num', None) else 'email'),
            method="POST",
            response=response,
            formxpath='//form[1]',
            formdata=formdata,
            callback=self.after_login,
            dont_click=True)

    def after_login(self, response):
        """the callback function after your login the zhihu
            by default this function will print out the login state code

        :param response: the response of the login page
        :return:None
        """
        import json
        result = json.loads(response.text)
        print(result)


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute('scrapy runspider {}'.format(__file__).split())
