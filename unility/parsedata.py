from datetime import datetime
import pandas as pd
import re
import bs4


def process_tag(tag):
    match tag.name:
        case 'img':
            return tag.get('title', '[图片]')
        case 'a':
            return f'[{tag.get_text()}]'
        case _:
            return tag.get_text()


def timestamp_to_datetime(timestamp_ms):
    # 将毫秒级时间戳转换为秒级时间戳
    timestamp_sec = timestamp_ms / 1000.0
    # 使用 datetime.fromtimestamp() 方法将秒级时间戳转换为日期时间对象
    dt_obj = datetime.fromtimestamp(timestamp_sec)
    # 使用 strftime() 方法将日期时间对象格式化为指定格式的字符串
    formatted_dt = dt_obj.strftime('%Y%m%d %H:%M:%S')
    return formatted_dt


def html2txt(html_content):
    soup = bs4.BeautifulSoup(html_content, features='html.parser')
    processed_text = ''.join(
        process_tag(tag) if isinstance(tag, bs4.Tag) else str(tag)
        for tag in soup.descendants
    )
    return processed_text


def remove_non_ascii(text):
    if isinstance(text, str):
        # 移除除了字母、数字、空格、逗号、句号、@ 符号和连字符之外的其他字符
        text = re.sub(r'\x08+', '', text)
        return text
    return str(text)


class UserInfo(object):
    def __init__(self, dict_data: dict | None):
        self._id = dict_data.get('id', None) if dict_data else None  # 用户id:数字
        self._screen_name = dict_data.get('screen_name', None) if dict_data else None  # 用户名称:字符串
        self._friends_count = dict_data.get('friends_count', None) if dict_data else None  # 关注用户数量:数字
        self._followers_count = dict_data.get('followers_count', None) if dict_data else None  # 粉丝数量:数字
        self._status_count = dict_data.get('status_count', None) if dict_data else None  # 发布帖子数量:数字
        self._stocks_count = dict_data.get('stocks_count', None) if dict_data else None  # 股票数量:数字
        self._province = dict_data.get('province', None) if dict_data else None  # 省份:字符串
        self._city = dict_data.get('city', None) if dict_data else None  # 市:字符串
        self._gender = dict_data.get('gender', None) if dict_data else None  # 性别:字符串
        self._description = dict_data.get('description', None) if dict_data else None  # 个人描述:字符串

    def __repr__(self):
        return f"UserInfo({vars(self)})"

    def to_dict(self):
        return vars(self)


class TextInfo(object):
    def __init__(self, dict_data: dict | None):
        self._id = dict_data.get('id', None) if dict_data else None  # 帖子id:数字
        self._user_id = dict_data.get('user_id', None) if dict_data else None  # 用户id:数字
        self._target = dict_data.get('target', None) if dict_data else None  # 帖子url，在地址前面加 'https://xueqiu.com':字符串
        # 对网址进行二次加工，在地址前面加 'https://xueqiu.com':字符串
        self._target = 'https://xueqiu.com{}'.format(self._target) if self._target else None
        self._source = dict_data.get('source', None) if dict_data else None  # 发帖设备:字符串
        self._created_at = dict_data.get('created_at', None) if dict_data else None  # 发帖时间，时间戳、毫秒:数字
        # 对时间戳进行二次加工，显示为可识别的时间格式
        self._created_at = timestamp_to_datetime(self._created_at) if self._created_at else None  # 发帖时间:字符串
        self._title = dict_data.get('title', None) if dict_data else None  # 标题:字符串
        self._retweet_count = dict_data.get('retweet_count', None) if dict_data else None  # 转发数量:数字
        self._reply_count = dict_data.get('reply_count', None) if dict_data else None  # 评论数量:数字
        self._like_count = dict_data.get('like_count', None) if dict_data else None  # 点赞数量:数字
        self._fav_count = dict_data.get('fav_count', None) if dict_data else None  # 收藏数量:数字
        self._commentId = dict_data.get('commentId', None) if dict_data else None  # 评论id:数字
        self._retweet_status_id = dict_data.get('retweet_status_id', None) if dict_data else None  # 被评论的文章id:数字
        self._stockCorrelation = dict_data.get('stockCorrelation', None) if dict_data else None  # 相关股票:列表
        self._text = dict_data.get('text', None) if dict_data else None  # 完整内容:字符串
        self._text = self._text if dict_data is None or self._text != '' \
            else dict_data.get('description', None)  # 如果text为空，则取description的值
        if self._text is not None:
            self._text = html2txt(self._text)

    def __repr__(self):
        return f"TextInfo({vars(self)})"

    def to_dict(self):
        return vars(self)


class StatusesInfo(object):
    def __init__(self, dict_data: dict | None):
        self.__parse_data_1(dict_data)
        self.__parse_data_2(dict_data)

    def __parse_data_1(self, dict_data: dict | None):
        self._text = TextInfo(dict_data)
        self._user = UserInfo(dict_data.get('user', None))
        if isinstance(dict_data, dict):
            self._text = TextInfo(dict_data if dict_data else None).to_dict()
            if isinstance(dict_data.get('user', None), dict):
                self._user = UserInfo(dict_data.get('user', None)).to_dict()

    def __parse_data_2(self, dict_data: dict | None):
        if isinstance(dict_data, dict):
            self._retweet_text = TextInfo(dict_data.get('retweeted_status', None)).to_dict()
            if isinstance(dict_data.get('retweeted_status', None), dict):
                self._retweet_user = UserInfo(dict_data.get('retweeted_status').get('user', None)).to_dict()

    def __repr__(self):
        return f"StatusesInfo({vars(self)})"

    def to_dict(self):
        return vars(self)


class ParseData(object):
    def __init__(self):
        self.statuses_list = list()

    def parse_statuses(self, xueqiu_page_json: dict):
        self.statuses_list.extend(map(lambda x: StatusesInfo(x).to_dict(), xueqiu_page_json['statuses']))

    def save_to_file(self, file_path: str):
        pd_list = map(lambda x: pd.json_normalize(x).map(remove_non_ascii), self.statuses_list)
        df = pd.concat(pd_list, sort=False)
        with pd.ExcelWriter(file_path) as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)
