import requests
import time
import json


def get_now_timestamp():
    milliseconds_timestamp = int(time.time() * 1000)
    return milliseconds_timestamp


class Network(object):
    def __set_cookie_my(self):
        with open('config.json', 'r') as file:
            config = json.load(file)
        for key, value in config['session'].items():
            self.__session.cookies.set(key, value, domain='.xueqiu.com')

    def __set_headers_my(self):
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,pt;q=0.6,zh-TW;q=0.5',
            'Connection': 'keep-alive',
            'Host': 'xueqiu.com',
            'Referer': 'https://xueqiu.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/125.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows'
        }
        self.__session.headers.update(headers)

    def __init__(self, user_id: str):
        self.__session = requests.session()
        self.__usr_id = user_id
        self.res = None
        self.__set_cookie_my()
        self.__set_headers_my()

    def get_page_url(self, page_num: int):
        page_url_base = 'https://xueqiu.com/v4/statuses/user_timeline.json?page={}&user_id={}&_={}'
        milliseconds_timestamp = get_now_timestamp()
        page_url = page_url_base.format(page_num, self.__usr_id, milliseconds_timestamp)
        self.res = self.__session.get(page_url)
        print(self.res.json())
