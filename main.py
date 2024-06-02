from unility import network
from unility import parsedata
import time
import datetime
import os


def get_desktop_path():
    home = os.path.expanduser("~")
    desktop = os.path.join(home, "Desktop")
    return desktop


if __name__ == '__main__':
    parse_data = parsedata.ParseData()
    net_my = network.Network('1247347556')  # 用户id，例如大道的id是1247347556
    for i in range(22, 23):
        print(i)
        net_my.get_page_url(i)
        res_json = net_my.res.json()
        parse_data.parse_statuses(res_json)
        time.sleep(2)
    desktop_path = get_desktop_path()
    parse_data.save_to_file(
        os.path.join(desktop_path, r'{}.xlsx'.format(datetime.datetime.now().strftime('%Y%m%d')))
    )


