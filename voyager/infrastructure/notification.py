from urllib.parse import urlencode
from configparser import ConfigParser
import datetime
import requests


class Notification(object):
    def __init__(self):
        print("【通知】读取通知配置")
        conf = ConfigParser()
        conf.read('../conf/notification.ini', encoding='UTF-8')

        self.push_server_url = conf.get('Notification', 'PushServerUrl')
        self.token = conf.get('Notification', 'Token')
        print("【通知】读取到的通知配置地址", self.push_server_url)

    def send(self, content):
        content += "-------------------" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        params = {'title': content, 'content': content, 'token': self.token}
        print("【通知】发送请求" + f'{self.push_server_url}?{urlencode(params)}')
        response = requests.get(f'{self.push_server_url}?{urlencode(params)}')
        if response.status_code == 200:
            print("【通知】通知发送成功")


if __name__ == '__main__':
    Notification().send('teest')
