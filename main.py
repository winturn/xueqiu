from unility import network
from unility import parsedata
import time
import datetime
import os
import warnings
from bs4 import MarkupResemblesLocatorWarning


def get_desktop_path():
    home = os.path.expanduser("~")
    desktop = os.path.join(home, "Desktop")
    return desktop


if __name__ == '__main__':
    warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
    parse_data = parsedata.ParseData()
    net_my = network.Network('1247347556')  # 用户id，例如大道的id是1247347556
    for i in range(1, 10):  # range的范围是 https://xueqiu.com/u/1247347556 页面的页数
        print(i)
        net_my.get_page_url(i)
        res_json = net_my.res.json()
        parse_data.parse_statuses(res_json)
        time.sleep(2)
    desktop_path = get_desktop_path()
    parse_data.save_to_file(
        # 文件保存到桌面，文件名为当前日期
        os.path.join(desktop_path, r'{}.xlsx'.format(datetime.datetime.now().strftime('%Y%m%d')))
    )


